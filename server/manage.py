import os, hashlib
from decimal import Decimal
from datetime import datetime
from flask.cli import FlaskGroup

from app import app, db
from app.auth.models import Users
from app.data.models import Trade_Log, Holding

cli = FlaskGroup(app)

@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()

def calculate_acb(operation, user_id, transaction, ticker, quantity, price, commission):
    try:
        pre_holding = Holding.query.filter_by(user_id=user_id, ticker=ticker).one()
        pre_quantity = pre_holding.quantity
        pre_acb = pre_holding.average_cost_basis
        pre_realized_gain = pre_holding.realized_gain
        Holding.query.filter_by(user_id=user_id, ticker=ticker).delete()
        db.session.commit()
    except:
        pre_quantity = 0
        pre_acb = 0
        pre_realized_gain = 0

    pre_quantity = Decimal(pre_quantity)
    pre_acb = Decimal(pre_acb)
    pre_realized_gain = Decimal(pre_realized_gain)
    quantity = Decimal(quantity)
    price = Decimal(price)
    commission = Decimal(commission)

    if operation == "Insert":
        if transaction == "Buy":
            post_quantity = pre_quantity + quantity
            post_acb = pre_acb + ((quantity * price) + commission)
            realized_gain = pre_realized_gain
        else:
            post_quantity = pre_quantity - quantity
            post_acb = pre_acb - (quantity * pre_acb/pre_quantity)
            realized_gain = pre_realized_gain + ((quantity * price) - commission)
    else:
        if transaction == "Buy":
            post_quantity = pre_quantity - quantity
            post_acb = pre_acb - ((quantity * price) + commission)
            realized_gain = pre_realized_gain
        else:
            post_quantity = pre_quantity + quantity
            post_acb = pre_acb + (quantity * pre_acb/pre_quantity)
            realized_gain = pre_realized_gain - ((quantity * price) - commission)

    if post_quantity != Decimal(0):
        post_acb_ps = post_acb / post_quantity
    else:
        post_acb_ps = Decimal(0)

    return int(post_quantity), Decimal(post_acb), Decimal(post_acb_ps), Decimal(realized_gain)

@cli.command("seed_db")
def seed_db():
    email = "luca.p.castelli@gmail.com"
    password = "test"
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    new_user = Users(username=email, salt=salt, key=key)
    db.session.add(new_user)
    db.session.commit()

    email = "sabena.quan@gmail.com"
    password = "pass"
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    new_user = Users(username=email, salt=salt, key=key)
    db.session.add(new_user)
    db.session.commit()

    person = Users.query.filter_by(username="luca.p.castelli@gmail.com").first()
    user_id = person.id

    date = datetime(2022,1,1)
    account = "Registered"
    transaction = "Buy"
    ticker = "AAPL"
    quantity = int(100)
    price = Decimal(95.05)
    commission = Decimal(9.99)
    post_quantity, post_acb, post_acb_ps, realized_gain = calculate_acb( "Insert", user_id, transaction, ticker, quantity, price, commission)
    db.session.add(Holding(user_id=user_id, account=account, ticker=ticker, quantity=post_quantity, average_cost_basis=post_acb, average_cost_basis_ps=post_acb_ps, realized_gain=realized_gain))
    db.session.add(Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission))
    db.session.commit()

    date = datetime(2022,1,10)
    account = "Registered"
    transaction = "Buy"
    ticker = "AAPL"
    quantity = int(200)
    price = Decimal(110.12)
    commission = Decimal(9.99)
    post_quantity, post_acb, post_acb_ps, realized_gain = calculate_acb( "Insert", user_id, transaction, ticker, quantity, price, commission)
    db.session.add(Holding(user_id=user_id, account=account, ticker=ticker, quantity=post_quantity, average_cost_basis=post_acb, average_cost_basis_ps=post_acb_ps, realized_gain=realized_gain))
    db.session.add(Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission))
    db.session.commit()

    date = datetime(2022,1,15)
    account = "Registered"
    transaction = "Sell"
    ticker = "AAPL"
    quantity = int(50)
    price = Decimal(130.60)
    commission = Decimal(9.99)
    post_quantity, post_acb, post_acb_ps, realized_gain = calculate_acb( "Insert", user_id, transaction, ticker, quantity, price, commission)
    db.session.add(Holding(user_id=user_id, account=account, ticker=ticker, quantity=post_quantity, average_cost_basis=post_acb, average_cost_basis_ps=post_acb_ps, realized_gain=realized_gain))
    db.session.add(Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission))
    db.session.commit()

    date = datetime(2022,1,20)
    account = "Registered"
    transaction = "Buy"
    ticker = "MSFT"
    quantity = int(100)
    price = Decimal(305)
    commission = Decimal(9.99)
    post_quantity, post_acb, post_acb_ps, realized_gain = calculate_acb( "Insert", user_id, transaction, ticker, quantity, price, commission)
    db.session.add(Holding(user_id=user_id, account=account, ticker=ticker, quantity=post_quantity, average_cost_basis=post_acb, average_cost_basis_ps=post_acb_ps, realized_gain=realized_gain))
    db.session.add(Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission))
    db.session.commit()


    # person = Users.query.filter_by(username="sabena.quan@gmail.com").first()
    # db.session.add(Trade_Log(user_id=person.id, date=datetime(2022,1,4), account="Registered", transaction="Buy", ticker="FB", quantity=55, price=10.55, commission=9.99))
    # db.session.add(Trade_Log(user_id=person.id, date=datetime(2022,1,9), account="Registered", transaction="Sell", ticker="FB", quantity=10, price=15.55, commission=9.99))
    # db.session.add(Trade_Log(user_id=person.id, date=datetime(2022,1,5), account="Registered", transaction="Buy", ticker="AAPL", quantity=20, price=85.05, commission=9.99))
    # db.session.commit()


if __name__ == "__main__":
    cli()