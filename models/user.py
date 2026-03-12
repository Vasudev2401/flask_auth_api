from extensions.db import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(120),unique=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime,server_default=db.func.now())
    role = db.Column(db.String(50),default="viewer")
    verification_token = db.Column(db.String)
    is_verified = db.Column(db.Boolean,default=False)