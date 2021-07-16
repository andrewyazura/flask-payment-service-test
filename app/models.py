from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class PaymentModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.String(280), nullable=False)
    currency = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(280), nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
