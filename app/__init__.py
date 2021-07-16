import logging

from config import Config
from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    logging.basicConfig(
        filename='flask-service.log',
        level=logging.INFO,
    )

    from app.models import db
    from app.routes import bp

    db.init_app(app)
    app.register_blueprint(bp)

    with app.app_context():
        from app.models import PaymentModel

        db.create_all()

    return app
