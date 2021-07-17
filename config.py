import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    SECRET_KEY = 'SecretKey01'
    SHOP_ID = 5

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        basedir, 'payments.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    IS_HEROKU = os.environ.get('IS_HEROKU')
