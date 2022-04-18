from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Email
from constants import *


class AddWalletForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    balance = IntegerField('Баланс', validators=[DataRequired()])
    main_currency = SelectField('Валюта', choices=REGISTRATION_PAGE_CURRENCIES_LIST)
    submit = SubmitField('Добавить')