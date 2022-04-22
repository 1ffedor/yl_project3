from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email
from constants import *


class AddTransactionForm(FlaskForm):
    transaction_sum = IntegerField('Сумма', validators=[DataRequired()])
    currency = SelectField('Валюта', choices=REGISTRATION_PAGE_CURRENCIES_LIST)
    wallet = SelectField('Счёт')
    comment = StringField('Название', validators=[DataRequired()])
    category = SelectField('Валюта', choices=REGISTRATION_PAGE_CURRENCIES_LIST)
    submit = SubmitField('Добавить')