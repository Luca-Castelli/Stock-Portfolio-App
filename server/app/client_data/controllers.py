from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app import db
from app.auth.models import Users
from app.client_data.models import Trade_Log, Holding
from app.market_data.models import Stock_Quote

client_data = Blueprint('client_data', __name__)

@client_data.route("/api/client_data/tradeLog", methods=["GET"])
@login_required
def trade_log():
    trade_log = Trade_Log.get_trade_log_for_user(user_id=current_user.id)
    
    if trade_log:
        trade_log = [i.serialize for i in trade_log]
        return jsonify(trade_log), 200
    else:
        return jsonify(None), 403

@client_data.route("/api/client_data/holdings", methods=["GET"])
@login_required
def holdings():
    holdings_stocks = Holding.holdings_with_stock_quotes(user_id=current_user.id)
    holdings_stocks = Holding.holdings_with_stock_quotes_serializer(holdings_stocks)
    if holdings_stocks:
        return jsonify(holdings_stocks), 200
    else:
        return jsonify(None), 403

@client_data.route("/api/client_data/tradeLogInsert", methods=["POST"])
@login_required
def trade_log_insert():
    date = request.json.get("date", None)
    account = request.json.get("account", None)
    transaction = request.json.get("transaction", None)
    symbol = request.json.get("symbol", None)
    quantity = int(request.json.get("quantity", None))
    price = Decimal(request.json.get("price", None))
    commission = Decimal(request.json.get("commission", None))

    success, stock_quote = Stock_Quote.create_stock_quote(symbol=symbol)
    if success:
        db.session.commit()

    user = Users.get_user_by_id(user_id=current_user.id)

    success, holding = Holding.create_holding(account=account, stock=stock_quote, user=user)
    if success:
        db.session.commit()

    if not holding.is_valid_transaction(operation="Insert", transaction=transaction, quantity=quantity):
        return jsonify("Adding trade would lead to negative shares held of " + symbol + "."), 403

    if holding.update(operation="Insert", transaction=transaction, quantity=quantity, price=price, commission=commission):
        db.session.commit()

    if Trade_Log.create_trade_log(date=date, account=account, transaction=transaction, quantity=quantity,
            price=price, commission=commission, stock=stock_quote, user=user):
        db.session.commit()
    
    return jsonify(None), 200

@client_data.route("/api/client_data/tradeLogRemove", methods=["POST"])
@login_required
def trade_log_remove():

    trade_id = request.json.get("trade_id", None)

    trade_log = Trade_Log.get_trade_log_by_id(trade_id=trade_id)

    holding = Holding.get_holdings_for_user_account_symbol(user_id=current_user.id, account=trade_log.account, symbol=trade_log.symbol)

    if not holding.is_valid_transaction(operation="Remove", transaction=trade_log.transaction, quantity=trade_log.quantity):
        return jsonify("Removing trade would lead to negative shares held of " + trade_log.symbol + "."), 403

    if holding.update(operation="Remove", transaction=trade_log.transaction, quantity=trade_log.quantity,
            price=trade_log.price, commission=trade_log.commission):
        db.session.commit()

    if trade_log.delete_trade_log():
        db.session.commit()
    
    return jsonify(None), 200