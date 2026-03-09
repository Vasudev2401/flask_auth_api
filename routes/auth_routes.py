from flask import Blueprint ,request ,make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.user import User
from extensions.db import db
from utils.password import hash_password, verify_password
from extensions.redis import redis_client
import os
from dotenv import load_dotenv

load_dotenv()

auth_bp = Blueprint("auth",__name__)
MAX_ATTEMPTS = int(os.getenv("LOGIN_ATTEMPTS_LIMIT"))
BLOCK_TIME = int(os.getenv("LOCKOUT_DURATION_SECONDS"))

@auth_bp.route("/register",methods=["POST"])
def register():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]
    if not email or not username or not password:
        return make_response({"message":"Missing Credentials"},400)
    hashed = hash_password("123456")
    user = User.query.filter_by(username=data["username"]).first()
    if user:
        return make_response({"message":"Username already exists"},409)
    user = User.query.filter_by(email=data["email"]).first()
    if user:
        return make_response({"message":"Email already exists"},409)
    user = User(
        username=data["username"],
        email = data["email"],
        password_hash = hashed
    )

    db.session.add(user)
    db.session.commit()

    return make_response({"message":"User registered successfully"},201)

@auth_bp.route('login',methods=["POST"])
def login():
    data = request.json
    username = data["username"]
    email = data["email"]
    password = data["password"]
    if not email or not username or not password:
        return make_response({"message":"Missing Credentials"},400)
    user = User.query.filter_by(username=data["username"],email=data["email"]).first()
    if not user:
        return make_response({"message":"No user found"},404)
    
    ip = request.remote_addr
    key = f"login_attempts:{ip}"
    attempts = redis_client.get(key)

    if attempts and int(attempts) >= MAX_ATTEMPTS:
        return make_response({"message":"Too many login attempts.Try again later"},429)
    
    if not verify_password(data["password"],user.password_hash):
        redis_client.incr(key)
        redis_client.expire(key,BLOCK_TIME)
        return make_response({"message":"Password not correct"},401)
    
    access_token = create_access_token(identity=str(user.id),additional_claims={
        "role":user.role
    })
    refresh_token = create_refresh_token(identity=str(user.id))
    return make_response({"access_token":access_token,"refresh_token":refresh_token,"message":"User logged in"},200)

@auth_bp.route("/profile")
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    print(user)
    return make_response({"Username":user.username,"Email":user.email},200)

@auth_bp.route("/refresh")
@jwt_required(refresh=True)
def refresh():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)
    new_access_token = create_access_token(identity = str(user_id),additional_claims={
        "role":user.role
    })
    return make_response({"new_access_token":new_access_token},200)

@auth_bp.route("/logout",methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    key = f"blocklist:{jti}"
    redis_client.set(key,"revoked",ex=3600)
    return make_response({"message":"Token blocked"})
