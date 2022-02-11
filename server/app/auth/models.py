import os, hashlib
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, LargeBinary, Boolean

from app import db

class Users(UserMixin, db.Model):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    active = Column(Boolean(), default=True, nullable=False)
    username = Column(String(128), unique=True, nullable=False)
    salt = Column(LargeBinary(256), nullable=False)
    key = Column(LargeBinary(256), nullable=False)

    trades = db.relationship("Trade_Log", backref='user')

    def __init__(self, username, salt, key):
        self.username = username
        self.salt = salt
        self.key = key

    @staticmethod
    def create_user(username, password):
        salt = os.urandom(32)
        key = Users.encrypt_password(password, salt)
        user = Users(
            username=username,
            salt=salt,
            key=key
        )
        try:
            db.session.add(user)
            return True
        except:
            return False

    @staticmethod
    def login(username, password):
        user = Users.query.filter_by(username=username).first()
        if user.validate_password(password):
            return user
        else:
            return None
    
    @staticmethod
    def get_user_by_id(user_id):
        return Users.query.filter_by(id=user_id).first()

    @staticmethod
    def encrypt_password(password, salt):
        return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

    def validate_password(self, password):
        salt = self.salt
        key = self.key
        test_key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        if test_key == key:
            return True
        else:
            return False
    
    @property
    def serialize(self):
        return {
            'id'        :self.id,
            'active'    :self.active,
            'username'  :self.username
        }

