from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, EmailField, SelectField, BooleanField, FileField
from wtforms.validators import DataRequired, Email
from constants import *


class LoginForm(FlaskForm):
    email = EmailField('Почта',  validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')