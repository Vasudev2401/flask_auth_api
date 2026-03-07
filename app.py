from config import Config
from extensions.jwt import jwt
from extensions.db import db
from flask import Flask
from flask_migrate import Migrate
from routes.auth_routes import auth_bp
from models.token_blocklist import TokenBlocklist

app = Flask(__name__)
app.config.from_object(Config)
try:
    db.init_app(app)
    jwt.init_app(app)
    migrate = Migrate(app,db)
    print("Connection established")
except:
    print("Error")

Migrate(app,db)

@jwt.token_in_blocklist_loader
def check_if_token_blocked(jwt_header,jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklist.query.filter_by(jti=jti).first()
    return token is not None

app.register_blueprint(auth_bp,url_prefix="/auth")

