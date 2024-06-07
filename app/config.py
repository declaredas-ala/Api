# app/config.py
class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/api"
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
