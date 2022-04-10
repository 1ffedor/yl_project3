from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Email
from constants import *


class RegisterForm(FlaskForm):
    email = EmailField('Почта',  validators=[DataRequired(), Email()])
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired()])
    # валюта
    avatar = FileField("Фото профиля")
    main_currency = SelectField('Валюта', choices=REGISTRATION_PAGE_CURRENCIES_LIST)
    submit = SubmitField('Зарегистрироваться')


class LoginForm(FlaskForm):
    email = EmailField('Почта',  validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')