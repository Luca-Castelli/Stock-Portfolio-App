import simplejson
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app import db

class Trade_Log(db.Model):
    __tablename__ = "trade_log"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    date = db.Column(db.DateTime, unique=False, nullable=False)
    account = db.Column(db.String(128), unique=False, nullable=False)
    transaction = db.Column(db.String(128), unique=False, nullable=False)
    ticker = db.Column(db.String(128), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    price = db.Column(db.Numeric(15,2), unique=False, nullable=False)
    commission = db.Column(db.Numeric(15,2), unique=False, nullable=False)

class Trade_Log_Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trade_Log
        json_module = simplejson

class Holding(db.Model):
    __tablename__ = "holding"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=False, nullable=False)
    account = db.Column(db.String(128), unique=False, nullable=False)
    ticker = db.Column(db.String(128), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    average_cost_basis = db.Column(db.Numeric(15,2), unique=False, nullable=False)
    average_cost_basis_ps = db.Column(db.Numeric(15,2), unique=False, nullable=False)
    realized_gain = db.Column(db.Numeric(15,2), unique=False, nullable=False)
    
class Holding_Schema(SQLAlchemyAutoSchema):
    class Meta:
        model = Holding
        json_module = simplejson
