from flask import redirect, render_template

from app import app

from .forms import PaymentForm


@app.route('/', methods=['GET', 'POST'])
def homepage():
    form = PaymentForm()

    if form.validate_on_submit():
        return 'hello'

    return render_template('payment.html', form=form)
