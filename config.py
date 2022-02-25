import os

class Config(object):
    _db = os.environ['DB_VAR']
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_db}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DB_ECHO = True
