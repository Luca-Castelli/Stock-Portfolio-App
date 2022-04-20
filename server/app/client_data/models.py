from ast import Num
from datetime import datetime
from re import T
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
        symbols = []
        for value in db.session.query(Trade_Log.symbol).filter(Trade_Log.user_id==user_id).distinct():
            symbols.append(value[0])
        return symbols
    
    @staticmethod
    def get_distinct_symbols():
        symbols = []
        for value in db.session.query(Trade_Log.symbol).distinct():
            symbols.append(value[0])
        return symbols  

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

        if not valuation_date:
            tz = timezone('EST')
            dt = datetime.now(tz)
            valuation_date = datetime(dt.year, dt.month, dt.day) - pd.tseries.offsets.BDay(0)

        trade_log = trade_log[trade_log['date'] <= valuation_date]

        if trade_log.empty:
            return trade_log

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

        try:
            trade_log['src_realized_gain_sell'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: (x['price'] - x['src_post_acb_ps']) * x['quantity'] - x['commission'] , axis=1)
        except:
            trade_log['src_realized_gain_sell'] = np.NaN
        try:
            trade_log['src_realized_gain_dividend'] = trade_log[trade_log["transaction"] == "Dividend"].apply(lambda x: x['price'], axis=1)
        except:
            trade_log['src_realized_gain_dividend'] = np.NaN
        try: 
            trade_log['cad_realized_gain_sell_fx'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: (x['price_fx'] - x['acb_fx']) * x['src_realized_gain_sell'] , axis=1)
        except:
            trade_log['cad_realized_gain_sell_fx'] =np.NaN
        try:
            trade_log['cad_realized_gain_sell'] = trade_log[trade_log["transaction"] == "Sell"].apply(lambda x: x['src_realized_gain_sell'] * x['price_fx'], axis=1)
        except:
            trade_log['cad_realized_gain_sell'] = np.NaN
        try:
            trade_log['cad_realized_gain_dividend'] = trade_log[trade_log["transaction"] == "Dividend"].apply(lambda x: x['price'] * x['price_fx'], axis=1)
        except:
            trade_log['cad_realized_gain_dividend'] = np.NaN

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

        # calculate market value
        holdings_stock_fx['src_market_value'] = holdings_stock_fx.apply(lambda x: x['price'] * x['post_qty'] , axis=1)
        holdings_stock_fx['cad_market_value'] = holdings_stock_fx.apply(lambda x: (x['price'] * x['post_qty']) * x['price_fx'], axis=1)

        # calculate unrealized pnl
        holdings_stock_fx['src_unrealized_gain'] = holdings_stock_fx.apply(lambda x: x['src_market_value'] - x['src_post_acb'] , axis=1)
        holdings_stock_fx['cad_unrealized_gain_fx'] = holdings_stock_fx.apply(lambda x: (x['price_fx'] - x['acb_fx']) * x['src_unrealized_gain'] , axis=1)
        holdings_stock_fx['cad_unrealized_gain'] = holdings_stock_fx.apply(lambda x: x['cad_market_value'] - x['cad_post_acb'], axis=1)

        # calculate unrealized pnl %
        try:
            holdings_stock_fx['cad_unrealized_gain_percent'] = holdings_stock_fx.apply(lambda x: (x['cad_unrealized_gain'] / x['cad_post_acb']) * 100, axis=1)
        except:
            holdings_stock_fx['cad_unrealized_gain_percent'] = 0
            
        # calculate total value
        cad_total_value = holdings_stock_fx['cad_market_value'].sum()

        # calculate weight
        holdings_stock_fx['weight'] = holdings_stock_fx.apply(lambda x: (x['cad_market_value'] / cad_total_value) * 100 , axis=1)

        return holdings_stock_fx

    @staticmethod
    def calculate_holdings_return(user_id, from_date, to_date=None):

        if not to_date:
            tz = timezone('EST')
            dt = datetime.now(tz)
            to_date = datetime(dt.year, dt.month, dt.day) - pd.tseries.offsets.BDay(0)

        trade_log = pd.read_sql(Trade_Log.query.filter_by(user_id=user_id).statement, db.session.bind)
        trade_log_period = trade_log[trade_log['date'] > from_date]
        trade_log_period = trade_log_period[trade_log_period['date'] <= to_date]

        fx = pd.read_sql(FX_Price.query.filter_by(date=from_date).statement, db.session.bind)
        trade_log_period = trade_log_period.merge(fx, how='left', left_on=['fx_symbol'], right_on=['symbol'], suffixes=(None, '_fx'))
        trade_log_period['price_fx'].fillna(1, inplace=True)

        try:
            trade_log_period['cad_buys'] = trade_log_period[trade_log_period["transaction"] == "Buy"].apply(lambda x: x['price_fx'] * (x['price'] * x['quantity'] + x['commission']), axis=1)
        except:
            trade_log_period['cad_buys'] = np.NaN
        try:
            trade_log_period['cad_sells'] = trade_log_period[trade_log_period["transaction"] == "Sell"].apply(lambda x: x['price_fx'] * (x['price'] * x['quantity'] - x['commission']), axis=1)
        except:
            trade_log_period['cad_sells'] = np.NaN
        try:
            trade_log_period['cad_divs'] = trade_log_period[trade_log_period["transaction"] == "Dividend"].apply(lambda x: x['price_fx'] * x['price'], axis=1)
        except:
            trade_log_period['cad_divs'] = np.NaN

        contributions = trade_log_period['cad_buys'].sum()
        withdrawls = trade_log_period['cad_sells'].sum()
        dividends = trade_log_period['cad_divs'].sum()

        t0_holdings = Trade_Log.construct_holdings(user_id=user_id, valuation_date=from_date)
        try:
            t0_cad_market_value = t0_holdings['cad_market_value'].sum()
        except:
            t0_cad_market_value = 0

        t1_holdings = Trade_Log.construct_holdings(user_id=user_id, valuation_date=to_date)
        try:
            t1_cad_market_value = t1_holdings['cad_market_value'].sum()
        except:
            t1_cad_market_value = 0
    
        return_period = t1_cad_market_value - t0_cad_market_value - contributions + withdrawls + dividends
        return_period_percent = (return_period / (t0_cad_market_value + contributions)) * 100

        return return_period, return_period_percent

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
            'fx_symbol'     : self.fx_symbol,
            'user_id'       : self.user_id
        }