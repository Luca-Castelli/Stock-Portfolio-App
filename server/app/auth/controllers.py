from flask import Blueprint, request, jsonify
from flask_wtf.csrf import generate_csrf
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app.auth.models import Users

auth = Blueprint('auth', __name__)

@auth.route("/api/auth/getCsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"detail": "CSRF cookie set"})
    response.headers.set("X-CSRFToken", token)
    return response, 200

@auth.route('/api/auth/getSession', methods=["GET"])
def get_session():
    if current_user.is_authenticated:
        return jsonify(None), 200
    else:
        return jsonify(None), 403

@auth.route('/api/auth/login', methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    user = Users.login(username=email, password=password)
    print(user)
    if user:
        login_user(user)
        return jsonify(None), 200
    else:
        return jsonify(None), 403

@auth.route('/api/auth/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return jsonify(None), 200

@auth.route('/api/auth/register', methods=["POST"])
def register():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if Users.create_user(username=email, password=password):
        db.session.commit()
        return jsonify(None), 200
    else:
        return jsonify(None), 403