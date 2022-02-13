from ast import Num
from datetime import datetime
from pytz import timezone
from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func

import numpy as np
import pandas as pd
pd.set_option('display.max_columns', None)

from app import db
from app.market_data.models import Stock_Price, FX_Price

class Trade_Log(db.Model):

    __tablename__ = "trade_log"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    account = Column(String(128), nullable=False)
    transaction = Column(String(128), nullable=False)
    symbol = Column(String(128), ForeignKey('stock.symbol'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15,2), nullable=False)
    commission = Column(Numeric(15,2), nullable=False)
    fx_symbol = Column(String(128), ForeignKey('fx.symbol'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, date, account, transaction, quantity, price, commission, stock, fx, user):
        self.date = date
        self.account = account
        self.transaction = transaction
        self.quantity = quantity
        self.price = price
        self.commission = commission
        self.stock = stock
        self.fx = fx
        self.user = user

    @staticmethod
    def insert_item(date, account, transaction, quantity, price, commission, stock, fx, user):
        
        if not Trade_Log.is_valid_transaction(operation="Insert", user_id=user.id, date=date, account=account, transaction=transaction, symbol=stock.symbol, quantity=quantity):
            return False

        trade_log = Trade_Log(
            date=date,
            account=account,
            transaction=transaction,
            quantity=quantity,
            price=price,
            commission=commission,
            stock=stock,
            fx=fx,
            user=user
        )
        try:
            db.session.add(trade_log)
            return True
        except:
            return False

    def delete_item(self):

        if not Trade_Log.is_valid_transaction(operation="Remove", user_id=self.user_id, date=self.date, account=self.account, transaction=self.transaction, symbol=self.symbol, quantity=self.quantity):
            return False

        try:
            Trade_Log.query.filter_by(id=self.id).delete()
            return True
        except:
            return False

    @staticmethod
    def get_trade_log_for_user(user_id):
        return Trade_Log.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_distinct_symbols_for_user(user_id):
        return db.session.query(Trade_Log).filter(Trade_Log.user_id==user_id).distinct(Trade_Log.symbol).group_by(Trade_Log.symbol).count()

    @staticmethod
    def get_trade_log_by_id(trade_id):
        return Trade_Log.query.filter_by(id=trade_id).first()
    
    @staticmethod
    def is_valid_transaction(operation, user_id, date, account, transaction, symbol, quantity):
        if (operation == "Insert" and transaction == "Sell"):
            buy_quantity_query = db.session.query(
                func.sum(Trade_Log.quantity).label('total_quantity')).filter(
                    Trade_Log.user_id==user_id, 
                    Trade_Log.date<=date,
                    Trade_Log.account==account, 
                    Trade_Log.transaction=="Buy", 
                    Trade_Log.symbol==symbol).first()

            sell_quantity_query = db.session.query(
                func.sum(Trade_Log.quantity).label('total_quantity')).filter(
                    Trade_Log.user_id==user_id, 
                    Trade_Log.date<=date,
                    Trade_Log.account==account, 
                    Trade_Log.transaction=="Sell", 
                    Trade_Log.symbol==symbol).first()

            if buy_quantity_query.total_quantity != None:
                buy_quantity = buy_quantity_query.total_quantity
            else:
                buy_quantity = 0

            if sell_quantity_query.total_quantity != None:
                sell_quantity = sell_quantity_query.total_quantity
            else:
                sell_quantity = 0

            net_quantity = buy_quantity - sell_quantity
            if net_quantity < quantity:
                return False

        if (operation == "Remove" and transaction == "Buy"):
            buy_quantity_query = db.session.query(
                func.sum(Trade_Log.quantity).label('total_quantity')).filter(
                    Trade_Log.user_id==user_id, 
                    Trade_Log.date<=date,
                    Trade_Log.account==account, 
                    Trade_Log.transaction=="Buy", 
                    Trade_Log.symbol==symbol).first()
            
            sell_quantity_query = db.session.query(
                func.sum(Trade_Log.quantity).label('total_quantity')).filter(
                    Trade_Log.user_id==user_id, 
                    Trade_Log.date>=date,
                    Trade_Log.account==account, 
                    Trade_Log.transaction=="Sell", 
                    Trade_Log.symbol==symbol).first()

            if buy_quantity_query.total_quantity != None:
                buy_quantity = buy_quantity_query.total_quantity
            else:
                buy_quantity = 0

            if sell_quantity_query.total_quantity != None:
                sell_quantity = sell_quantity_query.total_quantity
            else:
                sell_quantity = 0

            if (buy_quantity - quantity) < sell_quantity:
                return False

        return True

    @staticmethod
    def construct_holdings(user_id, valuation_date=None):

        trade_log = pd.read_sql(Trade_Log.query.filter_by(user_id=user_id).statement, db.session.bind)

        if valuation_date != None:
            trade_log = trade_log[trade_log['date'] <= valuation_date]
        else:
            tz = timezone('EST')
            dt = datetime.now(tz)
            valuation_date = datetime(dt.year, dt.month, dt.day) - pd.tseries.offsets.BDay(1)

        fx = pd.read_sql(FX_Price.query.statement, db.session.bind)

        trade_log = trade_log.merge(fx, how='left', left_on=['date', 'fx_symbol'], right_on=['date', 'symbol'], suffixes=(None, '_fx'))
        trade_log['price_fx'].fillna(1, inplace=True)

        trade_log.sort_values(['account', 'symbol', 'date'], ascending=[True, True, True], inplace=True)
        trade_log['src_total_amt'] = trade_log.apply(lambda x: ((x['quantity'] * x['price']) + x['commission']), axis = 1)
        trade_log['src_total_amt_ps'] = trade_log['src_total_amt'] / trade_log['quantity']
        trade_log['cad_total_amt'] = trade_log.apply(lambda x: ((x['quantity'] * x['price']) + x['commission']) * x['price_fx'], axis = 1)
        trade_log['cad_total_amt_ps'] = trade_log['cad_total_amt'] / trade_log['quantity']
        trade_log['adj_qty'] = trade_log.apply(lambda x: ((x['transaction'] == "Buy") - (x['transaction'] == "Sell")) * x['quantity'], axis = 1)
        trade_log['cum_qty'] = trade_log.groupby(['account','symbol'])['adj_qty'].cumsum()
        trade_log['src_cum_buys'] = trade_log[trade_log["transaction"] == "Buy"].groupby(['account', 'symbol'])['src_total_amt'].cumsum()
        trade_log['src_cum_buys_ps'] = trade_log['src_cum_buys'] / trade_log['cum_qty']
        trade_log['cad_cum_buys'] = trade_log[trade_log["transaction"] == "Buy"].groupby(['account', 'symbol'])['cad_total_amt'].cumsum()
        trade_log['cad_cum_buys_ps'] = trade_log['cad_cum_buys'] / trade_log['cum_qty']
        trade_log['pre_qty'] = trade_log.groupby(['account','symbol'])['cum_qty'].shift()
        trade_log['src_pre_acb'] = trade_log.groupby(['account', 'symbol', 'transaction'])['src_cum_buys'].shift()
        trade_log['src_pre_acb_ps'] = trade_log.groupby(['account', 'symbol', 'transaction'])['src_cum_buys_ps'].shift()
        trade_log['cad_pre_acb'] = trade_log.groupby(['account', 'symbol', 'transaction'])['cad_cum_buys'].shift()
        trade_log['cad_pre_acb_ps'] = trade_log.groupby(['account', 'symbol', 'transaction'])['cad_cum_buys_ps'].shift()
        trade_log['post_qty'] = trade_log['cum_qty']
        trade_log['src_post_acb'] = trade_log['src_pre_acb_ps'] * trade_log['pre_qty'] + trade_log['src_total_amt']
        trade_log['cad_post_acb'] = trade_log['cad_pre_acb_ps'] * trade_log['pre_qty'] + trade_log['cad_total_amt']
        trade_log['src_post_acb_ps'] = trade_log['src_post_acb'].divide(trade_log['post_qty']).fillna(trade_log['src_cum_buys_ps'])
        trade_log['src_post_acb_ps'].fillna(method='ffill', inplace=True)
        trade_log['src_pre_acb_ps'].fillna(trade_log['src_post_acb_ps'], inplace=True)
        trade_log['cad_post_acb_ps'] = trade_log['cad_post_acb'].divide(trade_log['post_qty']).fillna(trade_log['cad_cum_buys_ps'])
        trade_log['cad_post_acb_ps'].fillna(method='ffill', inplace=True)
        trade_log['cad_pre_acb_ps'].fillna(trade_log['cad_post_acb_ps'], inplace=True) 
        trade_log['src_post_acb'] = trade_log['src_post_acb_ps'] * trade_log['post_qty']
        trade_log['cad_post_acb'] = trade_log['cad_post_acb_ps'] * trade_log['post_qty']
        trade_log['acb_fx'] = trade_log['cad_post_acb_ps'] / trade_log['src_post_acb_ps']
        trade_log['src_realized_gain_sell'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: (x['price'] - x['src_post_acb_ps']) * x['quantity'] , axis=1)
        trade_log['src_realized_gain_dividend'] = trade_log[trade_log["transaction"] == "Dividend"].apply(lambda x: x['price'], axis=1)
        trade_log['cad_realized_gain_sell_fx'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: (x['price_fx'] - x['acb_fx']) * x['src_realized_gain_sell'] , axis=1)
        trade_log['cad_realized_gain_sell'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: x['src_realized_gain_sell'] * x['price_fx'], axis=1)
        trade_log['cad_realized_gain_dividend'] = trade_log[trade_log["transaction"] == "Dividend"].apply(lambda x: x['price'] * x['price_fx'], axis=1)

        holdings = trade_log.sort_values('date').drop_duplicates(['account', 'symbol'], keep='last')
        holdings = holdings[['account', 'symbol', 'fx_symbol', 'post_qty', 'src_post_acb_ps', 'cad_post_acb_ps', 'src_post_acb', 'cad_post_acb', 'acb_fx']].sort_values(['account', 'symbol']).reset_index()
        holdings['cad_realized_gain_sell_fx'] = trade_log.sort_values(['account', 'symbol']).groupby(['account', 'symbol']).sum().reset_index()['cad_realized_gain_sell_fx']
        holdings['cad_realized_gain_sell'] = trade_log.sort_values(['account', 'symbol']).groupby(['account', 'symbol']).sum().reset_index()['cad_realized_gain_sell']
        holdings['cad_realized_gain_dividend'] = trade_log.sort_values(['account', 'symbol']).groupby(['account', 'symbol']).sum().reset_index()['cad_realized_gain_dividend']

        stock_price = pd.read_sql(Stock_Price.query.filter_by(date=valuation_date).statement, db.session.bind)
        holdings_stock = holdings.merge(stock_price, how='left', left_on=['symbol'], right_on=['symbol'], suffixes=(None, '_stock'))

        fx = pd.read_sql(FX_Price.query.filter_by(date=valuation_date).statement, db.session.bind)
        holdings_stock_fx = holdings_stock.merge(fx, how='left', left_on=['fx_symbol'], right_on=['symbol'], suffixes=(None, '_fx'))
        holdings_stock_fx['price_fx'].fillna(1, inplace=True)
        
        holdings_stock_fx = holdings_stock_fx[['account', 'symbol', 'post_qty', 'src_post_acb_ps', 'cad_post_acb_ps', 'src_post_acb', 'cad_post_acb', 'acb_fx', 'cad_realized_gain_sell_fx', 'cad_realized_gain_sell', 'cad_realized_gain_dividend', 'price', 'price_fx']]
        print(holdings_stock_fx)

        # calculate unrealized pnl
        holdings['src_unrealized_gain'] = holdings.apply(lambda x: (x['price'] - x['src_post_acb_ps']) * x['quantity'] , axis=1)



    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'date'          : self.date.strftime("%Y-%m-%d"),
            'account'       : self.account,
            'transaction'   : self.transaction,
            'symbol'        : self.symbol,
            'quantity'      : f'{self.quantity}',
            'price'         : f'{self.price}',
            'commission'    : f'{self.commission}',
            'fx'            : self.fx,
            'user_id'       : self.user_id
        }

# class Holding(db.Model):

#     __tablename__ = "holding"

#     id = Column(Integer, primary_key=True)
#     account = Column(String(128), nullable=False)
#     symbol = Column(String(128), ForeignKey('stock.symbol'), nullable=False)
#     quantity = Column(Integer, nullable=False)
#     average_cost_basis = Column(Numeric(15,2), nullable=False)
#     average_cost_basis_ps = Column(Numeric(15,2), nullable=False)
#     realized_pnl = Column(Numeric(15,2), nullable=False)
#     dividends = Column(Numeric(15,2), nullable=False)
#     user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

#     def __init__(self, account, quantity, average_cost_basis, average_cost_basis_ps, realized_pnl, dividends, stock, user):
#         self.account = account
#         self.quantity = quantity
#         self.average_cost_basis = average_cost_basis
#         self.average_cost_basis_ps = average_cost_basis_ps
#         self.realized_pnl = realized_pnl
#         self.dividends = dividends
#         self.stock = stock
#         self.user = user

#     @staticmethod
#     def create_holding(account, stock, user):
#         exisiting_holding = Holding.get_holdings_for_user_account_symbol(user_id=user.id, account=account, symbol=stock.symbol)
#         if exisiting_holding:
#             return False, exisiting_holding

#         holding = Holding(
#             account=account,
#             quantity=0,
#             average_cost_basis=0,
#             average_cost_basis_ps=0,
#             realized_pnl=0,
#             dividends=0,
#             stock=stock,
#             user=user
#         )
#         try:
#             db.session.add(holding)
#             return True, holding
#         except:
#             return False, None
    
#     @staticmethod
#     def get_holdings_for_user(user_id):
#         return Holding.query.filter_by(user_id=user_id).all()

#     @staticmethod
#     def get_holdings_for_user_account_symbol(user_id, account, symbol):
#         return Holding.query.filter_by(user_id=user_id, account=account, symbol=symbol).first()

#     def update_holding(self, operation, transaction, quantity, price, commission):
#         new_quantity = self.quantity
#         new_acb = self.average_cost_basis
#         new_realized_pnl = self.realized_pnl
#         new_dividends = self.dividends
#         if operation == "Insert":
#             if transaction == "Buy":
#                 new_quantity = self.quantity + quantity
#                 new_acb = self.average_cost_basis + ((quantity * price) + commission)
#                 new_realized_pnl = self.realized_pnl
#             elif transaction == "Sell":
#                 new_quantity = self.quantity - quantity
#                 new_acb = self.average_cost_basis - (quantity * self.average_cost_basis/self.quantity)
#                 new_realized_pnl = self.realized_pnl + ((quantity * price) - commission)               
#             elif transaction == "Dividend":
#                 new_dividends = self.dividends + price
#         elif operation == "Remove":
#             if transaction == "Buy":
#                 new_quantity = self.quantity - quantity
#                 new_acb = self.average_cost_basis - ((quantity * price) + commission)
#                 new_realized_pnl = self.realized_pnl
#             elif transaction == "Sell":
#                 new_quantity = self.quantity + quantity
#                 new_acb = self.average_cost_basis + (quantity * self.average_cost_basis/self.quantity)
#                 new_realized_pnl = self.realized_pnl - ((quantity * price) - commission)
#             elif transaction == "Dividend":
#                 new_dividends = self.dividends - price

#         self.quantity = int(new_quantity)
#         self.average_cost_basis = new_acb
#         self.realized_pnl = new_realized_pnl
#         self.dividends = new_dividends
        
#         if(self.quantity > 0):
#             self.average_cost_basis_ps = self.average_cost_basis / self.quantity
#         else:
#             self.average_cost_basis_ps = 0
        
#         return True

#     @staticmethod
#     def holdings_with_stock_quotes(user_id):
#         holdings_stocks = db.session.query(Holding, Stock_).filter(user_id==user_id).join(Stock_Quote).all()
#         holdings_stocks = [list(x) for x in holdings_stocks]
#         return holdings_stocks

#     @staticmethod
#     def holdings_with_stock_quotes_calculated_fields(holdings_stocks):
#         calculated_fileds = []
#         total_market_value = 0
#         for pair in holdings_stocks:
#             output_item = {}
#             # market_value
#             quantity = pair[0].quantity
#             latest_price = pair[1].latest_price
#             market_value = quantity * latest_price
#             total_market_value += market_value
#             output_item.update({'market_value': market_value})
#              # unrealized_pnl
#             book_value = pair[0].average_cost_basis
#             unrealized_pnl = market_value - book_value
#             output_item.update({'unrealized_pnl': unrealized_pnl})
#             # unrealized_pnl_percent
#             if book_value == 0:
#                 unrealized_pnl_percent = 0
#             else:
#                 unrealized_pnl_percent = 100 * (unrealized_pnl / book_value)
#             output_item.update({'unrealized_pnl_percent': unrealized_pnl_percent})

#             calculated_fileds.append(output_item)

#         # weight
#         for item in calculated_fileds:
#             market_value = item['market_value']
#             if total_market_value == 0:
#                 weight = 0
#             else:
#                 weight = 100 * (market_value / total_market_value)
#             item.update({'weight': weight})
           
#         return calculated_fileds

#     @staticmethod
#     def holdings_with_stock_quotes_serializer(holdings_stocks, calculated_fields=None):
#         output_list = []
#         for pair in holdings_stocks:
#             output_item = {}
#             for item in pair:
#                 output_item.update(item.serialize)
#             output_list.append(output_item)

#         if calculated_fields and (len(output_list) == len(calculated_fields)):
#             for i in range(0,len(output_list)):
#                 for field in calculated_fields[i]:
#                     calculated_fields[i][field] = f'{calculated_fields[i][field]}'
#                 output_list[i].update(calculated_fields[i])
#         return output_list

#     @property
#     def serialize(self):
#         return {
#             'id'                    : self.id,
#             'account'               : self.account,
#             'symbol'                : self.symbol,
#             'quantity'              : f'{self.quantity}',
#             'average_cost_basis'    : f'{self.average_cost_basis}',
#             'average_cost_basis_ps' : f'{self.average_cost_basis_ps}',
#             'realized_pnl'          : f'{self.realized_pnl}',
#             'dividends'             : f'{self.dividends}',
#             'user_id'               : self.user_id
#         }