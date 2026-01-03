import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECREt_KEY", "dev_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("MYSQL_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
