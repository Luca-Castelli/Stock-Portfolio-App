from flask_login import UserMixin

from app import db

class Users(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    salt = db.Column(db.LargeBinary(256), unique=False, nullable=False)
    key = db.Column(db.LargeBinary(256), unique=False, nullable=False)

    trade_log = db.relationship("Trade_Log")
    holding = db.relationship("Holding")
