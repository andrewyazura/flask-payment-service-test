class Config(object):
    SECRET_KEY = 'SecretKey01'
    SHOP_ID = 5

    SQLALCHEMY_DATABASE_URI = 'sqlite:///../payments.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
