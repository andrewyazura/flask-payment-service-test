import logging

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
        logging.info('valid payment form received')

        data = form.data
        payment = PaymentModel(
            amount=str(data['amount']),
            currency=int(data['currency']),
            description=data['description'],
        )
        db.session.add(payment)
        db.session.commit()
        logging.debug('payment created')

        if data['currency'] == '840':
            logging.info('form currency is USD')
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
            logging.info('request to bill api sent')

            if response['result']:
                logging.info(
                    'request to bill api successful, redirecting user to received url'
                )
                return redirect(response['data']['url'])
            else:
                logging.error(
                    'request to api failed, error message: {}'.format(
                        response['message']
                    )
                )

        elif data['currency'] == '978':
            logging.info('form currency is EUR')
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
            logging.info('request to invoice api sent')

            if response['result']:
                logging.info(
                    'request to invoice api successful, redirecting user to invoice form'
                )
                return render_template('invoice.html', form_data=response['data'])
            else:
                logging.error(
                    'request to api failed, error message: {}'.format(
                        response['message']
                    )
                )

        elif data['currency'] == '643':
            logging.info('form currency is RUB')
            required_data = {
                'amount': str(data['amount']),
                'currency': int(data['currency']),
                'shop_id': current_app.config['SHOP_ID'],
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {**required_data, 'sign': hash, 'description': data['description']}

            logging.info('redirecting user to payment form')
            return render_template('pay.html', form_data=data)

    logging.info('rendering homepage')
    return render_template('homepage.html', form=form)
