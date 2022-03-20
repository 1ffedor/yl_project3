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
    # url_mdb_css = url_for('static', filename='css/mdb.min.css')
    # url_custom_css = url_for('static', filename='css/style.css')
    # url_mdb_js = url_for('static', filename='js/mdb.min.js')
    page_title = "mylbudget"
    return render_template("start_page.html", page_title=page_title)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    page_title = "Войти"
    return render_template("login_page.html", page_title=page_title)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)