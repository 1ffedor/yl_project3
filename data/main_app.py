# from data import db_session
# from data.users import User
# from data.news import News
from flask import Flask, url_for, render_template, redirect
import requests
from constants import *
# from forms.user import RegisterForm
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
def start_page():
    title = "Главная"
    # if login:
    #     pass  # если авторизован
    return render_template(MAIN_PAGE_HTML, title=title)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)