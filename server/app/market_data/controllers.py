from decimal import Decimal
from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from app import db
from app.market_data.models import Stock, Stock_Price


market_data = Blueprint('market_data', __name__)


@market_data.route("/api/market_data/symbols", methods=["GET"])
@login_required
def symbols():
    stocks = Stock.get_US_canadian_symbols()
    if stocks:
        stocks = [i.serialize for i in stocks]
        return jsonify(stocks), 200
    else:
        return jsonify(None), 403