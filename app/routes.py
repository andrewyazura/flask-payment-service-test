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
        current_app.logger.info('valid payment form received')

        data = form.data
        payment = PaymentModel(
            amount=str(data['amount']),
            currency=int(data['currency']),
            description=data['description'],
        )
        db.session.add(payment)
        db.session.commit()
        current_app.logger.info('payment created')

        if data['currency'] == '840':
            current_app.logger.info('form currency is USD')
            required_data = {
                'shop_id': current_app.config['SHOP_ID'],
                'shop_amount': str(data['amount']),
                'shop_currency': int(data['currency']),
                'payer_currency': int(data['currency']),
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {
                **required_data,
                'sign': hash,
                'description': data['description'],
            }
            response = requests.post(
                'https://core.piastrix.com/bill/create', json=data
            ).json()
            current_app.logger.info('request to bill api sent')

            if response['result']:
                current_app.logger.info(
                    'request to bill api successful, redirecting user to received url'
                )
                return redirect(response['data']['url'])
            else:
                current_app.logger.error(
                    'request to api failed, error message: {}'.format(
                        response['message']
                    )
                )

        elif data['currency'] == '978':
            current_app.logger.info('form currency is EUR')
            required_data = {
                'amount': str(data['amount']),
                'currency': int(data['currency']),
                'payway': 'advcash_rub',
                'shop_id': current_app.config['SHOP_ID'],
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {
                **required_data,
                'sign': hash,
                'description': data['description'],
            }
            response = requests.post(
                'https://core.piastrix.com/invoice/create', json=data
            ).json()
            current_app.logger.info('request to invoice api sent')

            if response['result']:
                current_app.logger.info(
                    'request to invoice api successful, redirecting user to invoice form'
                )
                return render_template(
                    'invoice.html', form_data=response['data']
                )
            else:
                current_app.logger.error(
                    'request to api failed, error message: {}'.format(
                        response['message']
                    )
                )

        elif data['currency'] == '643':
            current_app.logger.info('form currency is RUB')
            required_data = {
                'amount': str(data['amount']),
                'currency': int(data['currency']),
                'shop_id': current_app.config['SHOP_ID'],
                'shop_order_id': payment.id,
            }

            hash = generate_signature(required_data, current_app.secret_key)
            data = {
                **required_data,
                'sign': hash,
                'description': data['description'],
            }

            current_app.logger.info('redirecting user to payment form')
            return render_template('pay.html', form_data=data)

    current_app.logger.info('rendering homepage')
    return render_template('homepage.html', form=form)
