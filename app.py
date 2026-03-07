from config import Config
from extensions.jwt import jwt
from extensions.db import db
from flask import Flask
from flask_migrate import Migrate

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

