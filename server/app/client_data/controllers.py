from curses import use_default_colors
from decimal import Decimal
from datetime import datetime
import time
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app import db
from app.auth.models import Users
from app.client_data.models import Trade_Log
from app.market_data.models import Stock, Stock_Price, FX, FX_Price

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
    symbols = Trade_Log.get_distinct_symbols_for_user(user_id=current_user.id)
    Stock_Price.fetch_stock_prices(symbols)
    # FX_Price.fetch_fx_prices()
    holdings = Trade_Log.construct_holdings(user_id=current_user.id)
    holdings = holdings.to_json(orient='records')
    if holdings:
        return holdings, 200
    else:
        return jsonify(None), 403

@client_data.route("/api/client_data/returns", methods=['GET'])
@login_required
def returns():
    returns = {}
    time.sleep(1)
    returns['ytd'], returns['ytd_percent'] = Trade_Log.calculate_holdings_return(user_id=current_user.id, from_date=datetime(2021,12,31))
    returns['mtd'], returns['mtd_percent'] = Trade_Log.calculate_holdings_return(user_id=current_user.id, from_date=datetime(2022,1,31))
    returns['dtd'], returns['dtd_percent'] = Trade_Log.calculate_holdings_return(user_id=current_user.id, from_date=datetime(2022,2,14))
    return jsonify(returns), 200

@client_data.route("/api/client_data/tradeLogInsert", methods=["POST"])
@login_required
def trade_log_insert():
    date = datetime.strptime(request.json.get("date", None), '%Y-%m-%d')
    account = request.json.get("account", None)
    transaction = request.json.get("transaction", None)
    symbol = request.json.get("symbol", None)
    quantity = int(request.json.get("quantity", None))
    price = Decimal(request.json.get("price", None))
    commission = Decimal(request.json.get("commission", None))

    stock = Stock.get_stock_by_symbol(symbol=symbol)
    if stock.region == "US":
        fx_symbol = "USDCAD"
    else:
        fx_symbol = "CADCAD"
    fx = FX.get_fx_by_symbol(symbol=fx_symbol)
    user = Users.get_user_by_id(user_id=current_user.id)
    if Trade_Log.insert_item(date, account, transaction, quantity, price, commission, stock, fx, user):
        db.session.commit()
        return jsonify(None), 200
    else:
        return jsonify(None), 403

@client_data.route("/api/client_data/tradeLogRemove", methods=["POST"])
@login_required
def trade_log_remove():
    trade_id = request.json.get("trade_id", None)
    trade_log = Trade_Log.get_trade_log_by_id(trade_id=trade_id)
    print(trade_log)
    if trade_log.delete_item():
        db.session.commit()
        return jsonify(None), 200
    else:
        return jsonify(None), 403