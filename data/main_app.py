from data import db_session
from data.users import User
# from data.news import News
from flask import Flask, url_for, render_template, redirect
import requests
from constants import *
from forms.user import RegisterForm
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/blogs.db")


@app.route('/')
def start_page():
    # url_mdb_css = url_for('static', filename='css/mdb.min.css')
    # url_custom_css = url_for('static', filename='css/style.css')
    # url_mdb_js = url_for('static', filename='js/mdb.min.js')
    page_title = "mylbudget"
    return render_template("start_page.html", page_title=page_title)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    page_title = "Авторизация"
    return render_template("login_page.html", page_title=page_title)


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    page_title = "Регистрация"
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template("registration_page.html", page_title=page_title, form=form)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)