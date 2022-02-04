from sqlalchemy import Column, Integer, String, Numeric

from app import db

class Market_Universe(db.Model):

    __tablename__ = "market_universe"

    symbol = Column(String(128), primary_key=True)
    exchange = Column(String(128), nullable=False)
    exchange_name = Column(String(128), nullable=False)
    name = Column(String(1024), nullable=False)
    type = Column(String(128), nullable=False)
    region = Column(String(128), nullable=False)
    currency = Column(String(128), nullable=False)

    def __init__(self, symbol, exchange, exchange_name, name, type, region, currency):
        self.symbol = symbol
        self.exchange = exchange
        self.exchange_name = exchange_name
        self.name = name
        self.type = type
        self.region = region
        self.currency = currency

    @property
    def serialize(self):
        return {
            'symbol'    : self.symbol,
            'name'      : self.name,
            'type'      : self.type,
            'region'    : self.region,
        }
    
class Stock_Quote(db.Model):

    __tablename__ = "stock_quote"

    symbol = Column(String(128), primary_key=True)
    latest_price = Column(Numeric(15,2))
    # latest_time = Column(String(128), unique=False, nullable=True)
    # avg_total_volume = Column(String(128), unique=False, nullable=True)
    # change = Column(Numeric(15,2), unique=False, nullable=True)
    # change_percent = Column(Numeric(15,2), unique=False, nullable=True)
    # currency = Column(String(128), unique=False, nullable=True)
    # market_cap = Column(String(128), unique=False, nullable=True)
    # pe_ratio = Column(Integer, unique=False, nullable=True)
    # previous_close = Column(Numeric(15,2), unique=False, nullable=True)
    # previous_volume = Column(String(128), unique=False, nullable=True)
    # week_52_low = Column(Numeric(15,2), unique=False, nullable=True)
    # week_52_high = db.Column(Numeric(15,2), unique=False, nullable=True)
    # ytd_change = db.Column(Numeric(15,2), unique=False, nullable=True)
    trades = db.relationship("Trade_Log", backref='stock')
    holdings = db.relationship("Holding", backref='stock')

    def __init__(self, symbol, latest_price):
        self.symbol = symbol
        self.latest_price = latest_price

    @staticmethod
    def create_stock_quote(symbol, latest_price=None):
        exisiting_stock_quote = Stock_Quote.get_stock_quote(symbol=symbol)
        if exisiting_stock_quote:
            return False, exisiting_stock_quote
            
        stock_quote = Stock_Quote(
            symbol = symbol,
            latest_price = latest_price,
        )
        try:
            db.session.add(stock_quote)
            return True, stock_quote
        except:
            return False, None
    
    @staticmethod
    def get_stock_quote(symbol):
        return Stock_Quote.query.filter_by(symbol=symbol).first()

    @property
    def serialize(self):
        return {
            'symbol'            : self.symbol,
            'latest_price'      : f'{self.latest_price}',
        }