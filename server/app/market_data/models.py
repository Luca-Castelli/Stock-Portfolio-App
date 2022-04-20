from decimal import Decimal
from datetime import datetime
import yfinance as yf
import pandas as pd
from sqlalchemy import Column, String, Numeric, ForeignKey, DateTime, Integer, or_

from app import db

# IEX_TOKEN = "pk_8d6cdabb7dae46bcb9ca3e44ea3174c2"
# IEX_BATCH_QUOTE = "https://cloud.iexapis.com/stable/stock/market/batch"
# IEX_QUOTE = "https://cloud.iexapis.com/stable/stock/"
# IEX_SYMBOLS = ["https://cloud.iexapis.com/stable/ref-data/region/US/symbols", 
# "https://cloud.iexapis.com/stable/ref-data/region/CA/symbols"]

class Stock(db.Model):

    __tablename__ = "stock"

    symbol = Column(String(128), primary_key=True)
    exchange = Column(String(128), nullable=False)
    exchange_name = Column(String(128), nullable=False)
    name = Column(String(1024), nullable=False)
    type = Column(String(128), nullable=False)
    region = Column(String(128), nullable=False)
    currency = Column(String(128), nullable=False)

    trades = db.relationship("Trade_Log", backref='stock')
    prices = db.relationship("Stock_Price", backref='stock')

    def __init__(self, symbol, exchange, exchange_name, name, type, region, currency):
        self.symbol = symbol
        self.exchange = exchange
        self.exchange_name = exchange_name
        self.name = name
        self.type = type
        self.region = region
        self.currency = currency

    @staticmethod
    def create_stock(symbol, exchange, exchange_name, name, type, region, currency):
        stock = Stock(
            symbol=symbol,
            exchange=exchange,
            exchange_name=exchange_name,
            name=name,
            type=type,
            region=region,
            currency=currency,
        )
        try:
            db.session.add(stock)
            return True, stock
        except:
            return False, None

    @staticmethod
    def populate_stocks():
        Stock.query.delete()
        db.session.commit()
        ca = pd.read_json('./app/assets/ca_symbols.json', orient='records')
        us = pd.read_json('./app/assets/us_symbols.json', orient='records')
        stocks = pd.concat([ca,us],ignore_index=True)
        stocks = stocks.set_index('symbol')
        stocks = stocks[['exchange', 'exchangeName', 'name', 'type', 'region', 'currency']]
        stocks = stocks.rename(columns={'exchangeName':'exchange_name'})
        stocks.to_sql('stock', db.session.bind, if_exists='append')
        return True

    @staticmethod
    def get_US_canadian_symbols():
        return db.session.query(Stock).filter(
            or_(Stock.type == "cs", Stock.type == "et")).all()

    @staticmethod
    def get_stock_by_symbol(symbol):
        return Stock.query.filter_by(symbol=symbol).first()

    @property
    def serialize(self):
        return {
            'symbol'    : self.symbol,
            'name'      : self.name,
            'type'      : self.type,
            'region'    : self.region,
        }
    
class Stock_Price(db.Model):

    __tablename__ = "stock_price"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(128), ForeignKey('stock.symbol'))
    date = Column(DateTime, nullable=False)
    price = Column(Numeric(15,2), nullable=False)

    def __init__(self, stock, date, price):
        self.stock = stock
        self.date = date
        self.price = price

    @staticmethod
    def create_stock_price(stock, date, price):
        stock_price = Stock_Price(
            stock=stock,
            date=date,
            price = price,
        )
        try:
            db.session.add(stock_price)
            return True, stock_price
        except:
            return False, None
    
    @staticmethod
    def get_stock_price(symbol, date):
        return Stock_Price.query.filter_by(symbol=symbol, date=date).first()

    @staticmethod
    def fetch_stock_prices(symbols=None):
        Stock_Price.query.delete()
        db.session.commit()
        if symbols:
            for symbol in symbols:
                stock = yf.Ticker(symbol)
                stock_h = stock.history(period="max")
                stock_d = stock_h.reset_index()
                stock_d['symbol'] = symbol
                stock_d = stock_d.set_index('symbol')
                stock_d = stock_d[['Close', 'Date']]
                stock_d = stock_d.rename(columns={'Close':'price', 'Date':'date'})
                stock_d.to_sql('stock_price', db.session.bind, if_exists='append')
        else:
            for stock in Stock.get_US_canadian_symbols():
                symbol = stock.symbol
                stock = yf.Ticker(symbol)
                stock_h = stock.history(period="max")
                stock_d = stock_h.reset_index()
                stock_d['symbol'] = symbol
                stock_d = stock_d.set_index('symbol')
                stock_d = stock_d[['Close', 'Date']]
                stock_d = stock_d.rename(columns={'Close':'price', 'Date':'date'})
                stock_d.to_sql('stock_price', db.session.bind, if_exists='append')
        return True
    
    @property
    def serialize(self):
        return {
            'symbol'            : self.symbol,
            'date'              : self.date.strftime("%Y-%m-%d"),
            'price'             : f'{self.price}',
        }

class FX(db.Model):

    __tablename__ = "fx"

    symbol = Column(String(128), primary_key=True)

    trades = db.relationship("Trade_Log", backref='fx')
    prices = db.relationship("FX_Price", backref='fx')

    def __init__(self, symbol):
        self.symbol = symbol

    @staticmethod
    def create_fx(symbol):
        fx = FX(
            symbol=symbol,
        )
        try:
            db.session.add(fx)
            return True, fx
        except:
            return False, None

    @staticmethod
    def populate_fx():
        success, fx = FX.create_fx(symbol="CADCAD")
        success, fx = FX.create_fx(symbol="USDCAD")
        if success:
            db.session.commit()
        return True

    @staticmethod
    def get_fx_by_symbol(symbol):
        return FX.query.filter_by(symbol=symbol).first()

    @property
    def serialize(self):
        return {
            'symbol'    : self.symbol,
        }
    
class FX_Price(db.Model):

    __tablename__ = "fx_price"

    id = Column(Integer, primary_key=True)
    symbol = Column(String(128), ForeignKey('fx.symbol'))
    date = Column(DateTime, nullable=False)
    price = Column(Numeric(15,4), nullable=False)

    def __init__(self, fx, date, price):
        self.fx = fx
        self.date = date
        self.price = price

    @staticmethod
    def create_fx_price(fx, date, price):
        fx_price = FX_Price(
            fx=fx,
            date=date,
            price = price,
        )
        try:
            db.session.add(fx_price)
            return True, fx_price
        except:
            return False, None
    
    @staticmethod
    def get_fx_price(symbol, date):
        return Stock_Price.query.filter_by(symbol=symbol, date=date).first()

    @staticmethod
    def fetch_fx_prices():
        FX_Price.query.delete()
        db.session.commit()
        usdcad = yf.Ticker("USDCAD=x")
        usdcad_h = usdcad.history(period="max")
        usdcad_d = usdcad_h.reset_index()
        usdcad_d['symbol'] = "USDCAD"
        usdcad_d = usdcad_d.set_index('symbol')
        usdcad_d = usdcad_d[['Close', 'Date']]
        usdcad_d = usdcad_d.rename(columns={'Close':'price', 'Date':'date'})
        usdcad_d.to_sql('fx_price', db.session.bind, if_exists='append')
        return True
    
    @property
    def serialize(self):
        return {
            'symbol'            : self.symbol,
            'date'              : self.date.strftime("%Y-%m-%d"),
            'price'             : f'{self.price}',
        }
