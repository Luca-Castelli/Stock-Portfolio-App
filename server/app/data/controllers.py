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

    holding_quantity, holding_acb, holding_acb_ps = holding_insert_acb(user_id, transaction, ticker, quantity, price, commission)
    new_holding = Holding(user_id=user_id, account=account, ticker=ticker, quantity=holding_quantity, average_cost_basis=holding_acb, average_cost_basis_ps=holding_acb_ps)
    db.session.add(new_holding)
    db.session.commit()

    new_trade = Trade_Log(user_id=user_id, date=date, account=account, transaction=transaction, ticker=ticker, quantity=quantity, price=price, commission=commission)
    db.session.add(new_trade)
    db.session.commit()

    return jsonify("Successfully added new trade"), 200

@data.route("/api/data/tradeLogRemove", methods=["POST"])
@login_required
def trade_log_remove():
    user_id = current_user.id
    trade_id = request.json.get("trade_id", None)
    Trade_Log.query.filter_by(id=trade_id, user_id=user_id).delete()
    db.session.commit()
    return jsonify("Successfully deleted trade"), 200

def holding_insert_acb(user_id, transaction, ticker, quantity, price, commission):
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

    if transaction == "Buy":
        post_quantity = pre_quantity + quantity
        post_acb = pre_acb + (quantity * price) + commission
    else:
        post_quantity = pre_quantity - quantity
        post_acb = pre_acb - (quantity * pre_acb/pre_quantity)

    post_acb_ps = post_acb / post_quantity

    return int(post_quantity), Decimal(post_acb), Decimal(post_acb_ps)
