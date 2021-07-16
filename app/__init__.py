import logging
import sys

from config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.models import db
    from app.routes import bp

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        from app.models import PaymentModel

        db.create_all()

    if app.config['IS_HEROKU']:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        app.logger.handlers.clear()
        app.logger.addHandler(stream_handler)
    else:
        logging.basicConfig(
            filename='flask-service.log',
            level=logging.INFO,
        )

    app.logger.setLevel(logging.INFO)
    app.logger.info('flask service starting')

    return app
