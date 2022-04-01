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
db_session.global_init("db/app_users.db")


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
    message = ""
    html_file = "registration_page.html"
    have_errors = False

    # сами названия классов
    my_0 = 'my-0'
    is_valid = my_0 + " is-valid"  # my-0 чтоб не было отступа
    is_invalid = "is-invalid"

    # словарь значений котореы добавляются в класссы инпутов для показания где все верно а где ошбика
    input_errors = {
        "email": {
            "errclass": "",
            "invalid-feedback": ""},
        "username": {
            "errclass": "",
            "invalid-feedback": ""},
        "password": {
            "errclass": "",
            "invalid-feedback": ""},
        "password_again": {
            "errclass": "",
            "invalid-feedback": ""}
    }

    form = RegisterForm()

    if form.validate_on_submit():
        # данные из полей
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        password_again = form.password_again.data

        for key in input_errors.keys():
            # проход по всем инпутам и даем им si valid
            input_errors[key]["errclass"] = is_valid

        if password != password_again:
            # если пароли не совпадают
            have_errors = True
            input_from = "password"

            message = "Пароли не совпадают!"

            input_errors[input_from]["errclass"] = is_invalid
            input_errors[f"{input_from}_again"]["errclass"] = is_invalid

            input_errors["password"]["invalid-feedback"] = message
            input_errors[f"{input_from}_again"]["invalid-feedback"] = message

        db_sess = db_session.create_session()

        if db_sess.query(User).filter(User.email == email).first():
            # проверка на наличие уже зарегистрированного с таким майлом
            have_errors = True
            input_from = "email"

            message = "Пользователь с таким email уже есть!"

            input_errors[input_from]["errclass"] = is_invalid
            input_errors[input_from]["invalid-feedback"] = message

        if db_sess.query(User).filter(User.username == username).first():
            # проверка на наличие пользователя с таким логином
            have_errors = True
            input_from = "username"

            message = "Пользователь с таким логином уже есть!"

            input_errors[input_from]["errclass"] = is_invalid
            input_errors[input_from]["invalid-feedback"] = message

        if have_errors:
            # если есть ошибки выводим
            return render_template(html_file, page_title=page_title, form=form, input_errors=input_errors)
        # иначе записываем в бд и редиректим
        user = User(email=email, username=username)
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        return redirect('/')

    return render_template(html_file, page_title=page_title, form=form, input_errors=input_errors)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)