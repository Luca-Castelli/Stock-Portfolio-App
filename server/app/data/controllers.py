from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app import db
from app.data.models import Trade_Log, Trade_Log_Schema, Holding, Holding_Schema

data = Blueprint('data', __name__)

@data.route("/api/data/tradeLog", methods=["GET"])
@login_required
def trade_log():
    user_id = current_user.id
    trade_log = Trade_Log.query.filter_by(user_id=user_id).all()
    trade_log_schema = Trade_Log_Schema(many=True)
    trade_log_json = trade_log_schema.dumps(trade_log)
    return jsonify(trade_log_json), 200

@data.route("/api/data/holdings", methods=["GET"])
@login_required
def holdings():
    user_id = current_user.id
    holdings = Holding.query.filter_by(user_id=user_id).all()
    holdings_schema = Holding_Schema(many=True)
    holdings_json = holdings_schema.dumps(holdings)
    return jsonify(holdings_json), 200

@data.route("/api/data/tradeLogInsert", methods=["POST"])
@login_required
def trade_log_insert():
    user_id = current_user.id
    date = request.json.get("date", None)
    account = request.json.get("account", None)
    transaction = request.json.get("transaction", None)
    ticker = request.json.get("ticker", None)
    quantity = request.json.get("quantity", None)
    price = request.json.get("price", None)
    commission = request.json.get("commission", None)

    if is_transaction_valid("Insert", user_id, transaction, ticker, int(quantity)) == False:
        msg = f"Failed to add trade. Adding would bring your {ticker} share count below zero."
        return jsonify(msg), 404

    holding_quantity, holding_acb, holding_acb_ps = calculate_acb("Insert", user_id, transaction, ticker, quantity, price, commission)
    new_holding = Holding(user_id=user_id, account=account, ticker=ticker, quantity=holding_quantity, average_cost_basis=holding_acb, average_cost_basis_ps=holding_acb_ps)
    db.session.add(new_holding)
    db.session.commit()

    new_trade = Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission)
    db.session.add(new_trade)
    db.session.commit()

    return jsonify("Successfully logged a new trade."), 200

@data.route("/api/data/tradeLogRemove", methods=["POST"])
@login_required
def trade_log_remove():
    user_id = current_user.id
    trade_id = request.json.get("trade_id", None)

    existing_trade = Trade_Log.query.filter_by(id=trade_id, user_id=user_id).one()
    account = existing_trade.account
    transaction = existing_trade.transaction
    ticker = existing_trade.ticker
    quantity = existing_trade.quantity
    price = existing_trade.price
    commission = existing_trade.commission

    if is_transaction_valid("Remove", user_id, transaction, ticker, int(quantity)) == False:
        msg = f"Failed to remove trade. Adding would bring your {ticker} share count below zero."
        return jsonify(msg), 404

    holding_quantity, holding_acb, holding_acb_ps = calculate_acb("Remove", user_id, transaction, ticker, quantity, price, commission)
    new_holding = Holding(user_id=user_id, account=account, ticker=ticker, quantity=holding_quantity, average_cost_basis=holding_acb, average_cost_basis_ps=holding_acb_ps)
    db.session.add(new_holding)
    db.session.commit()

    Trade_Log.query.filter_by(id=trade_id, user_id=user_id).delete()
    db.session.commit()

    return jsonify("Successfully removed a trade."), 200

def is_transaction_valid(operation, user_id, transaction, ticker, quantity):
    if (operation == "Insert" and transaction == "Sell") or (operation == "Remove" and transaction == "Buy"):
        try:
            pre_holding = Holding.query.filter_by(user_id=user_id, ticker=ticker).one()
            pre_quantity = pre_holding.quantity
            if(pre_quantity < quantity):
                return False
        except:
            return False
    return True
    
def calculate_acb(operation, user_id, transaction, ticker, quantity, price, commission):
    try:
        pre_holding = Holding.query.filter_by(user_id=user_id, ticker=ticker).one()
        pre_quantity = pre_holding.quantity
        pre_acb = pre_holding.average_cost_basis
        Holding.query.filter_by(user_id=user_id, ticker=ticker).delete()
        db.session.commit()
    except:
        pre_quantity = 0
        pre_acb = 0

    pre_quantity = Decimal(pre_quantity)
    pre_acb = Decimal(pre_acb)
    quantity = Decimal(quantity)
    price = Decimal(price)
    commission = Decimal(commission)

    if operation == "Insert":
        if transaction == "Buy":
            post_quantity = pre_quantity + quantity
            post_acb = pre_acb + ((quantity * price) + commission)
        else:
            post_quantity = pre_quantity - quantity
            post_acb = pre_acb - (quantity * pre_acb/pre_quantity)
    else:
        if transaction == "Buy":
            post_quantity = pre_quantity - quantity
            post_acb = pre_acb - ((quantity * price) + commission)
        else:
            post_quantity = pre_quantity + quantity
            post_acb = pre_acb + (quantity * pre_acb/pre_quantity)

    if post_quantity != Decimal(0):
        post_acb_ps = post_acb / post_quantity
    else:
        post_acb_ps = Decimal(0)

    return int(post_quantity), Decimal(post_acb), Decimal(post_acb_ps)