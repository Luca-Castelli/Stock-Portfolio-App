from decimal import Decimal
from datetime import datetime
from flask.cli import FlaskGroup

from app import app, db
from app.auth.models import Users
from app.client_data.models import Trade_Log
from app.market_data.models import Stock, Stock_Price, FX, FX_Price


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_users")
def seed_users():
    email = "luca.p.castelli@gmail.com"
    password = "test"
    if Users.create_user(username=email, password=password):
        db.session.commit()

    email = "sabena.quan@gmail.com"
    password = "pass"
    if Users.create_user(username=email, password=password):
        db.session.commit()

@cli.command("seed_stocks")
def seed_stocks():
    symbol = "AAPL"
    exchange = "NYSE"
    exchange_name = "New York Stock Exchange"
    name = "Apple Inc."
    type = "cs"
    region = "US"
    currency = "USD"
    stock = Stock(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(stock)
    db.session.commit()

    symbol = "MSFT"
    exchange = "NYSE"
    exchange_name = "New York Stock Exchange"
    name = "Microsoft Inc."
    type = "cs"
    region = "US"
    currency = "USD"
    stock = Stock(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(stock)
    db.session.commit()

    symbol = "GLO.TO"
    exchange = "TSX"
    exchange_name = "Toronto Stock Exchange"
    name = "Global Atomic Corp."
    type = "cs"
    region = "CA"
    currency = "CAD"
    stock = Stock(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(stock)
    db.session.commit()

@cli.command("seed_fx")
def seed_fx():
    FX.populate_fx()

@cli.command("seed_trade_log")
def seed_trade_log():

    user = Users.get_user_by_id(1)
    date = datetime(2022,1,4)
    account = "Registered"
    transaction = "Buy"
    symbol = "AAPL"
    quantity = int(100)
    price = Decimal(95.05)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()

    user = Users.get_user_by_id(1)
    date = datetime(2022,1,10)
    account = "Registered"
    transaction = "Buy"
    symbol = "AAPL"
    quantity = int(200)
    price = Decimal(110.12)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()

    user = Users.get_user_by_id(1)
    date = datetime(2022,1,17)
    account = "Registered"
    transaction = "Sell"
    symbol = "AAPL"
    quantity = int(50)
    price = Decimal(130.60)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()
    
    user = Users.get_user_by_id(1)
    date = datetime(2022,1,18)
    account = "Registered"
    transaction = "Buy"
    symbol = "AAPL"
    quantity = int(50)
    price = Decimal(111.60)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()

    user = Users.get_user_by_id(1)
    date = datetime(2022,1,20)
    account = "Registered"
    transaction = "Buy"
    symbol = "MSFT"
    quantity = int(100)
    price = Decimal(305)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()

    user = Users.get_user_by_id(1)
    date = datetime(2022,1,20)
    account = "Non-Registered"
    transaction = "Buy"
    symbol = "GLO.TO"
    quantity = int(1000)
    price = Decimal(3.05)
    commission = Decimal(9.99)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "CADCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()
    
    user = Users.get_user_by_id(1)
    date = datetime(2022,2,11)
    account = "Registered"
    transaction = "Dividend"
    symbol = "AAPL"
    quantity = int(1)
    price = Decimal(50)
    commission = Decimal(0)
    stock = Stock.get_stock_by_symbol(symbol=symbol)
    fx_symbol = "USDCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    if Trade_Log.insert_item(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock, fx=fx, user=user):
        db.session.commit()


@cli.command("seed_stock_prices")
def seed_stock_prices():

    # symbol = "GLO-CT"
    # stock = Stock.get_stock_by_symbol(symbol=symbol)
    # date = "2022-02-10"
    # price = 3.5
    # if Stock_Price.create_stock_price(stock, date, price):
    #     db.session.commit()
    
    # symbol = "MSFT"
    # stock = Stock.get_stock_by_symbol(symbol=symbol)
    # date = "2022-02-10"
    # price = 300
    # if Stock_Price.create_stock_price(stock, date, price):
    #     db.session.commit()

    # symbol = "AAPL"
    # stock = Stock.get_stock_by_symbol(symbol=symbol)
    # date = "2022-02-10"
    # price = 200
    # if Stock_Price.create_stock_price(stock, date, price):
    #     db.session.commit()
    Stock_Price.fetch_stock_prices(['AAPL','MSFT','GLO.TO'])

@cli.command("seed_fx_prices")
def seed_fx_prices():
    FX_Price.fetch_fx_prices()

@cli.command('test')
def test():
    Trade_Log.construct_holdings(1)

if __name__ == "__main__":
    cli()