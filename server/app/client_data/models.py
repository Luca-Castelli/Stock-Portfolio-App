from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func


from app import db
from app.market_data.models import Stock_Quote

class Trade_Log(db.Model):

    __tablename__ = "trade_log"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    account = Column(String(128), nullable=False)
    transaction = Column(String(128), nullable=False)
    symbol = Column(String(128), ForeignKey('stock_quote.symbol'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(15,2), nullable=False)
    commission = Column(Numeric(15,2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, date, account, transaction, quantity, price, commission, stock, user):
        self.date = date
        self.account = account
        self.transaction = transaction
        self.quantity = quantity
        self.price = price
        self.commission = commission
        self.stock = stock
        self.user = user

    @staticmethod
    def create_trade_log(date, account, transaction, quantity, price, commission, stock, user):
        trade_log = Trade_Log(
            date=date,
            account=account,
            transaction=transaction,
            quantity=quantity,
            price=price,
            commission=commission,
            stock=stock,
            user=user
        )
        try:
            db.session.add(trade_log)
            return True
        except:
            return False

    def delete_trade_log(self):
        try:
            Trade_Log.query.filter_by(id=self.id).delete()
            return True
        except:
            return False

    @staticmethod
    def get_trade_log_for_user(user_id):
        return Trade_Log.query.filter_by(user_id=user_id).all()

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
            'user_id'       : self.user_id
        }

class Holding(db.Model):

    __tablename__ = "holding"

    id = Column(Integer, primary_key=True)
    account = Column(String(128), nullable=False)
    symbol = Column(String(128), ForeignKey('stock_quote.symbol'), nullable=False)
    quantity = Column(Integer, nullable=False)
    average_cost_basis = Column(Numeric(15,2), nullable=False)
    average_cost_basis_ps = Column(Numeric(15,2), nullable=False)
    realized_pnl = Column(Numeric(15,2), nullable=False)
    dividends = Column(Numeric(15,2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, account, quantity, average_cost_basis, average_cost_basis_ps, realized_pnl, dividends, stock, user):
        self.account = account
        self.quantity = quantity
        self.average_cost_basis = average_cost_basis
        self.average_cost_basis_ps = average_cost_basis_ps
        self.realized_pnl = realized_pnl
        self.dividends = dividends
        self.stock = stock
        self.user = user

    @staticmethod
    def create_holding(account, stock, user):
        exisiting_holding = Holding.get_holdings_for_user_account_symbol(user_id=user.id, account=account, symbol=stock.symbol)
        if exisiting_holding:
            return False, exisiting_holding

        holding = Holding(
            account=account,
            quantity=0,
            average_cost_basis=0,
            average_cost_basis_ps=0,
            realized_pnl=0,
            dividends=0,
            stock=stock,
            user=user
        )
        try:
            db.session.add(holding)
            return True, holding
        except:
            return False, None
    
    @staticmethod
    def get_holdings_for_user(user_id):
        return Holding.query.filter_by(user_id=user_id).all()

    @staticmethod
    def get_holdings_for_user_account_symbol(user_id, account, symbol):
        return Holding.query.filter_by(user_id=user_id, account=account, symbol=symbol).first()

    def update(self, operation, transaction, quantity, price, commission):
        new_quantity = self.quantity
        new_acb = self.average_cost_basis
        new_realized_pnl = self.realized_pnl
        new_dividends = self.dividends
        if operation == "Insert":
            if transaction == "Buy":
                new_quantity = self.quantity + quantity
                new_acb = self.average_cost_basis + ((quantity * price) + commission)
                new_realized_pnl = self.realized_pnl
            elif transaction == "Sell":
                new_quantity = self.quantity - quantity
                new_acb = self.average_cost_basis - (quantity * self.average_cost_basis/self.quantity)
                new_realized_pnl = self.realized_pnl + ((quantity * price) - commission)               
            elif transaction == "Dividend":
                new_dividends = self.dividends + price
        elif operation == "Remove":
            if transaction == "Buy":
                new_quantity = self.quantity - quantity
                new_acb = self.average_cost_basis - ((quantity * price) + commission)
                new_realized_pnl = self.realized_pnl
            elif transaction == "Sell":
                new_quantity = self.quantity + quantity
                new_acb = self.average_cost_basis + (quantity * self.average_cost_basis/self.quantity)
                new_realized_pnl = self.realized_pnl - ((quantity * price) - commission)
            elif transaction == "Dividend":
                new_dividends = self.dividends - price

        self.quantity = int(new_quantity)
        self.average_cost_basis = new_acb
        self.realized_pnl = new_realized_pnl
        self.dividends = new_dividends
        
        if(self.quantity > 0):
            self.average_cost_basis_ps = self.average_cost_basis / self.quantity
        else:
            self.average_cost_basis_ps = 0
        
        return True

    @staticmethod
    def holdings_with_stock_quotes(user_id):
        holdings_stocks = db.session.query(Holding, Stock_Quote).filter(user_id==user_id).join(Stock_Quote).all()
        holdings_stocks = [list(x) for x in holdings_stocks]
        return holdings_stocks

    @staticmethod
    def holdings_with_stock_quotes_calculated_fields(holdings_stocks):
        calculated_fileds = []
        total_market_value = 0
        for pair in holdings_stocks:
            output_item = {}
            # market_value
            quantity = pair[0].quantity
            latest_price = pair[1].latest_price
            market_value = quantity * latest_price
            total_market_value += market_value
            output_item.update({'market_value': market_value})
             # unrealized_pnl
            book_value = pair[0].average_cost_basis
            unrealized_pnl = market_value - book_value
            output_item.update({'unrealized_pnl': unrealized_pnl})
            # unrealized_pnl_percent
            if book_value == 0:
                unrealized_pnl_percent = 0
            else:
                unrealized_pnl_percent = unrealized_pnl / book_value
            output_item.update({'unrealized_pnl_percent': unrealized_pnl_percent})

            calculated_fileds.append(output_item)

        # weight
        for item in calculated_fileds:
            market_value = item['market_value']
            if total_market_value == 0:
                weight = 0
            else:
                weight = market_value / total_market_value
            item.update({'weight': weight})
           
        return calculated_fileds

    @staticmethod
    def holdings_with_stock_quotes_serializer(holdings_stocks, calculated_fields=None):
        output_list = []
        for pair in holdings_stocks:
            output_item = {}
            for item in pair:
                output_item.update(item.serialize)
            output_list.append(output_item)

        if calculated_fields and (len(output_list) == len(calculated_fields)):
            for i in range(0,len(output_list)):
                for field in calculated_fields[i]:
                    calculated_fields[i][field] = f'{calculated_fields[i][field]}'
                output_list[i].update(calculated_fields[i])
        return output_list

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'account'               : self.account,
            'symbol'                : self.symbol,
            'quantity'              : f'{self.quantity}',
            'average_cost_basis'    : f'{self.average_cost_basis}',
            'average_cost_basis_ps' : f'{self.average_cost_basis_ps}',
            'realized_pnl'          : f'{self.realized_pnl}',
            'dividends'             : f'{self.dividends}',
            'user_id'               : self.user_id
        }