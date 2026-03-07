import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRES_MINUTES")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRES_DAYS")))