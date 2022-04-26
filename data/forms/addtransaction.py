from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, DateTimeLocalField
from wtforms.validators import DataRequired
from constants import *
import datetime


class AddTransactionForm(FlaskForm):
    transaction_sum = IntegerField('Сумма', validators=[DataRequired()])
    # currency = StringField('Валюта')
    wallet = SelectField('Счёт')
    comment = StringField('Название', validators=[DataRequired()])
    transaction_expenses_category = SelectField('Категория', choices=CABINET_TRANSACTIONS_PAGE_EXPENSES_CATEGORIES_LIST)  # расход
    transaction_income_category = SelectField('Категория', choices=CABINET_TRANSACTIONS_PAGE_INCOME_CATEGORIES_LIST)  # доход
    transaction_date = DateTimeLocalField('Posted:', default=datetime.datetime.today, format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Добавить')