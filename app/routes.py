import hashlib

import requests
from flask import redirect, render_template

from app import app

from .forms import PaymentForm


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
            sign = (
                ':'.join(
                    [str(required_data[key]) for key in sorted(required_data.keys())]
                )
                + app.secret_key
            )
            hash = hashlib.sha256(sign.encode()).hexdigest()
            data = {**required_data, 'sign': hash, 'description': data['description']}
            response = requests.post(
                'https://core.piastrix.com/bill/create', json=data
            ).json()

            if response['result']:
                return redirect(response['data']['url'])
            else:
                print(response['message'])

        return 'hello'

    return render_template('payment.html', form=form)
