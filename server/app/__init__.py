from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.from_object("app.config.Config")

db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)
csrf = CSRFProtect(app)

from app.data.controllers import data as data_module
from app.auth.controllers import auth as auth_module

app.register_blueprint(auth_module)
app.register_blueprint(data_module)

from app.auth.models import Users
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))