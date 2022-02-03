from decimal import Decimal
from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey

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

    @property
    def serialize(self):
        return {
            'id'            : self.id,
            'date'          : self.date.strftime("%Y-%m-%d"),
            'account'       : self.account,
            'transaction'   : self.transaction,
            'symbol'        : self.symbol,
            'quantity'      : f'{self.quantity:,}',
            'price'         : f'{self.price:,.2f}',
            'commission'    : f'{self.commission:,.2f}',
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
    realized_gain = Column(Numeric(15,2), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __init__(self, account, quantity, average_cost_basis, average_cost_basis_ps, realized_gain, stock, user):
        self.account = account
        self.quantity = quantity
        self.average_cost_basis = average_cost_basis
        self.average_cost_basis_ps = average_cost_basis_ps
        self.realized_gain = realized_gain
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
            realized_gain=0,
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

    def is_valid_transaction(self, operation, transaction, quantity):
        if (operation == "Insert" and transaction == "Sell") or (operation == "Remove" and transaction == "Buy"):
            if self.quantity < quantity:
                return False
        return True

    def update(self, operation, transaction, quantity, price, commission):
        if operation == "Insert":
            if transaction == "Buy":
                new_quantity = self.quantity + quantity
                new_acb = self.average_cost_basis + ((quantity * price) + commission)
                new_realized_gain = self.realized_gain
            else:
                new_quantity = self.quantity - quantity
                new_acb = self.average_cost_basis - (quantity * self.average_cost_basis/self.quantity)
                new_realized_gain = self.realized_gain + ((quantity * price) - commission)               
        elif operation == "Remove":
            if transaction == "Buy":
                new_quantity = self.quantity - quantity
                new_acb = self.average_cost_basis - ((quantity * price) + commission)
                new_realized_gain = self.realized_gain
            else:
                new_quantity = self.quantity + quantity
                new_acb = self.average_cost_basis + (quantity * self.average_cost_basis/self.quantity)
                new_realized_gain = self.realized_gain - ((quantity * price) - commission)

        self.quantity = int(new_quantity)
        self.average_cost_basis = new_acb
        self.realized_gain = new_realized_gain
        
        if(self.quantity > 0):
            self.average_cost_basis_ps = self.average_cost_basis / self.quantity
        else:
            self.average_cost_basis_ps = 0
        
        return True

    @staticmethod
    def holdings_with_stock_quotes(user_id):
        return db.session.query(Holding, Stock_Quote).filter(user_id==user_id).join(Stock_Quote).all()

    @staticmethod
    def holdings_with_stock_quotes_serializer(holdings_stocks):
        holdings_stocks = [list(x) for x in holdings_stocks]
        output_list = []
        for pair in holdings_stocks:
            output_item = {}
            for item in pair:
                output_item.update(item.serialize)
            output_list.append(output_item)
        return output_list

    # @staticmethod
    # def holdings_with_stock_quotes_calculated_fields(holding_stocks):
    #     for holding in holding_stocks:
    #         holding.update({'market_value':holding})

    @property
    def serialize(self):
        return {
            'id'                    : self.id,
            'account'               : self.account,
            'symbol'                : self.symbol,
            'quantity'              : f'{self.quantity:,}',
            'average_cost_basis'    : f'{self.average_cost_basis:,.2f}',
            'average_cost_basis_ps' : f'{self.average_cost_basis_ps:,.2f}',
            'realized_gain'         : f'{self.realized_gain:,.2f}',
            'user_id'               : self.user_id
        }