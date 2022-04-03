from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField
from wtforms.validators import DataRequired, Email
from constants import *


class RegisterForm(FlaskForm):
    email = EmailField('Почта',  validators=[DataRequired(), Email()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    # валюта
    currency = SelectField('Валюта', choices=CURRENCIES_LIST)
    submit = SubmitField('Зарегистрироваться')