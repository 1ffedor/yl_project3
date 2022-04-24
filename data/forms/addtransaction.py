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
    transaction_type = SelectField('Тип', choices=TRANSACTION_CATEGORIES_LIST)
    transaction_date = DateTimeLocalField('Posted:', default=datetime.datetime.today, format='%Y-%m-%dT%H:%M', validators=[DataRequired()])
    submit = SubmitField('Добавить')