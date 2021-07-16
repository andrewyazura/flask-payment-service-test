import requests
from flask import Blueprint, current_app, redirect, render_template

from app.forms import PaymentForm
from app.helpers import generate_signature
from app.models import PaymentModel, db

bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
def homepage():
    form = PaymentForm()

    if form.validate_on_submit():
        data = form.data
        payment = PaymentModel(
            amount=str(data['amount']),
            currency=int(data['currency']),
            description=data['description'],
        )
        db.session.add(payment)
        db.session.commit()

        if data['currency'] == '840':
            required_data = {
                'shop_id': current_app.config['SHOP_ID'],
                'shop_amount': str(data['amount']),
                'shop_currency': int(data['currency']),
                'payer_currency': int(data['currency']),
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {**required_data, 'sign': hash, 'description': data['description']}
            response = requests.post(
                'https://core.piastrix.com/bill/create', json=data
            ).json()

            if response['result']:

                return redirect(response['data']['url'])
            else:
                print(response['message'])

        elif data['currency'] == '978':
            required_data = {
                'amount': str(data['amount']),
                'currency': int(data['currency']),
                'payway': 'advcash_rub',
                'shop_id': current_app.config['SHOP_ID'],
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {**required_data, 'sign': hash, 'description': data['description']}
            response = requests.post(
                'https://core.piastrix.com/invoice/create', json=data
            ).json()

            if response['result']:

                return render_template('invoice.html', form_data=response['data'])
            else:
                print(response['message'])

        elif data['currency'] == '643':
            required_data = {
                'amount': str(data['amount']),
                'currency': int(data['currency']),
                'shop_id': current_app.config['SHOP_ID'],
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {**required_data, 'sign': hash, 'description': data['description']}

            return render_template('pay.html', form_data=data)

    return render_template('homepage.html', form=form)
