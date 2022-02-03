from decimal import Decimal
from datetime import datetime
from flask.cli import FlaskGroup

from app import app, db
from app.auth.models import Users
from app.client_data.models import Trade_Log, Holding
from app.market_data.models import Market_Universe, Stock_Quote


cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

@cli.command("seed_db")
def seed_db():
    email = "luca.p.castelli@gmail.com"
    password = "test"
    if Users.create_user(username=email, password=password):
        db.session.commit()

    email = "sabena.quan@gmail.com"
    password = "pass"
    if Users.create_user(username=email, password=password):
        db.session.commit()

    user = Users.get_user_by_id(1)

    date = datetime(2022,1,1)
    account = "Registered"
    transaction = "Buy"
    symbol = "AAPL"
    quantity = int(100)
    price = Decimal(95.05)
    commission = Decimal(9.99)
    latest_price = Decimal(565.55)
    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol, latest_price=latest_price)
    if success:
        db.session.commit()
    user = Users.get_user_by_id(user_id=user.id)
    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()
    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()
    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()

    date = datetime(2022,1,10)
    account = "Registered"
    transaction = "Buy"
    symbol = "AAPL"
    quantity = int(200)
    price = Decimal(110.12)
    commission = Decimal(9.99)
    latest_price = Decimal(211.55)
    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol, latest_price=latest_price)
    if success:
        db.session.commit()
    user = Users.get_user_by_id(user_id=user.id)
    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()
    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()
    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()

    date = datetime(2022,1,15)
    account = "Registered"
    transaction = "Sell"
    symbol = "AAPL"
    quantity = int(50)
    price = Decimal(130.60)
    commission = Decimal(9.99)
    latest_price = Decimal(13.55)
    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol, latest_price=latest_price)
    if success:
        db.session.commit()
    user = Users.get_user_by_id(user_id=user.id)
    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()
    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()
    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()

    date = datetime(2022,1,20)
    account = "Registered"
    transaction = "Buy"
    symbol = "MSFT"
    quantity = int(100)
    price = Decimal(305)
    commission = Decimal(9.99)
    latest_price = Decimal(12.55)
    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol, latest_price=latest_price)
    if success:
        db.session.commit()
    user = Users.get_user_by_id(user_id=user.id)
    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()
    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()
    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()

    date = datetime(2022,1,20)
    account = "Non-Registered"
    transaction = "Buy"
    symbol = "GLO-CT"
    quantity = int(1000)
    price = Decimal(3.05)
    commission = Decimal(9.99)
    latest_price = Decimal(2.55)
    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol, latest_price=latest_price)
    if success:
        db.session.commit()
    user = Users.get_user_by_id(user_id=user.id)
    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()
    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()
    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()

    symbol = "AAPL"
    exchange = "NYSE"
    exchange_name = "New York Stock Exchange"
    name = "Apple Inc."
    type = "cs"
    region = "US"
    currency = "USD"
    universe = Market_Universe(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(universe)
    db.session.commit()

    symbol = "MSFT"
    exchange = "NYSE"
    exchange_name = "New York Stock Exchange"
    name = "Microsoft Inc."
    type = "cs"
    region = "US"
    currency = "USD"
    universe = Market_Universe(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(universe)
    db.session.commit()

    symbol = "GLO-CT"
    exchange = "TSX"
    exchange_name = "Toronto Stock Exchange"
    name = "Global Atomic Corp."
    type = "cs"
    region = "CA"
    currency = "CAD"
    universe = Market_Universe(symbol, exchange, exchange_name, name, type, region, currency)
    db.session.add(universe)
    db.session.commit()


if __name__ == "__main__":
    cli()