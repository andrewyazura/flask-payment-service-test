import hashlib

import requests
from flask import redirect, render_template

from app import app

from .forms import PaymentForm
from .helpers import generate_signature


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = PaymentForm()

    if form.validate_on_submit():
        data = form.data

        if data['currency'] == '840':
            required_data = {
                'shop_id': app.config['SHOP_ID'],
                'shop_amount': str(data['amount']),
                'shop_currency': int(data['currency']),
                'payer_currency': int(data['currency']),
                'shop_order_id': 1234,
            }

            hash = generate_signature(required_data, app.secret_key)
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
                'shop_id': app.config['SHOP_ID'],
                'shop_order_id': 1234,
            }

            hash = generate_signature(required_data, app.secret_key)
            data = {**required_data, 'sign': hash, 'description': data['description']}
            response = requests.post(
                'https://core.piastrix.com/invoice/create', json=data
            ).json()

            if response['result']:
                return render_template('invoice.html', form_data=response['data'])
            else:
                print(response['message'])

    return render_template('homepage.html', form=form)
