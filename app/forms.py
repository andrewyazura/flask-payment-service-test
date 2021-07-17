from flask_wtf import FlaskForm
from wtforms.fields import DecimalField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Optional
from wtforms.widgets import TextArea


class PaymentForm(FlaskForm):
    amount = DecimalField(
        u'Amount',
        validators=[DataRequired()],
    )
    currency = SelectField(
        u'Currency',
        choices=[(840, 'USD'), (978, 'EUR'), (643, 'RUB')],
        validators=[DataRequired()],
    )
    description = StringField(
        u'Description',
        widget=TextArea(),
        validators=[Optional()],
    )
    submit = SubmitField(u'Pay')
