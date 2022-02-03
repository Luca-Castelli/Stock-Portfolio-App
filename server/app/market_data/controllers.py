from decimal import Decimal
import requests
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required
from sqlalchemy import or_

from app import db
from app.market_data.models import Market_Universe, Stock_Quote

IEX_TOKEN = "pk_8d6cdabb7dae46bcb9ca3e44ea3174c2"
IEX_QUOTE = "https://cloud.iexapis.com/stable/stock/market/batch"
IEX_SYMBOLS = ["https://cloud.iexapis.com/stable/ref-data/region/US/symbols", 
"https://cloud.iexapis.com/stable/ref-data/region/CA/symbols"]

market_data = Blueprint('market_data', __name__)

def populate_market_universe():
    urls = [item + "?token=" + IEX_TOKEN for item in IEX_SYMBOLS]
    for url in urls:
        response = requests.get(url)
        data = response.json()
        for d in data:
            new_market_universe = Market_Universe(symbol=d['symbol'], exchange=d['exchange'], exchange_name=d['exchangeName'],
            name=d['name'], type=d['type'], region=d['region'], currency=d['currency'])
            db.session.add(new_market_universe)
    db.session.commit()

@market_data.route("/api/market_data/symbols", methods=["GET"])
@login_required
def symbols():
    market_universe = db.session.query(Market_Universe).filter(or_(Market_Universe.type == "cs", Market_Universe.type == "et")).all()
    if market_universe:
        market_universe = [i.serialize for i in market_universe]
        return jsonify(market_universe), 200
    else:
        return jsonify(None), 403

def insert_to_stock_quote(symbol):
    exisiting_stock_quote = Stock_Quote.query.filter_by(symbol=symbol).first()
    if not exisiting_stock_quote:
        new_stock_quote = Stock_Quote(symbol=symbol)
        db.session.add(new_stock_quote)
        db.session.commit()
        return new_stock_quote
    return exisiting_stock_quote

def populate_stock_quote(symbols):
    symbols_str = ','.join(symbols)
    url = IEX_QUOTE + "?symbols=" + symbols_str + "&types=quote" + "&token=" + IEX_TOKEN
    response = requests.get(url)
    data = response.json()
    for symbol in symbols:
        stock_quote = Stock_Quote.query.filter_by(symbol=data[symbol]['quote']['symbol']).first()
        stock_quote.latest_price = Decimal(data[symbol]['quote']['latestPrice'])
        # stock_quote.latest_time = str(data[symbol]['quote']['latestTime'])
        # stock_quote.avg_total_volume = str(data[symbol]['quote']['avgTotalVolume'])
        # stock_quote.change = Decimal(data[symbol]['quote']['change'])
        # stock_quote.change_percent = Decimal(data[symbol]['quote']['changePercent'])
        # stock_quote.currency = str(data[symbol]['quote']['currency'])
        # stock_quote.market_cap = str(data[symbol]['quote']['marketCap'])
        # stock_quote.pe_ratio = int(data[symbol]['quote']['peRatio'])
        # stock_quote.previous_close = Decimal(data[symbol]['quote']['previousClose'])
        # stock_quote.previous_volume = str(data[symbol]['quote']['previousVolume'])
        # stock_quote.week_52_low = Decimal(data[symbol]['quote']['week52Low'])
        # stock_quote.week_52_high = Decimal(data[symbol]['quote']['week52High'])
        # stock_quote.ytd_change = Decimal(data[symbol]['quote']['ytdChange'])
        db.session.commit()