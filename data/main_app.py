from data import db_session
from data.users import User
from data.wallets import Wallet
from data.transactions import Transaction
from flask import Flask, url_for, render_template, redirect, request
import flask_login
from flask_login import LoginManager, login_user, login_required, logout_user
from werkzeug.utils import secure_filename
import requests
from constants import *
from forms.login import LoginForm
from forms.registration import RegisterForm
from forms.addwallet import AddWalletForm
from forms.addtransaction import AddTransactionExpensesForm, AddTransactionIncomeForm
import json
import datetime
from func_app import *


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(
#     days=30
# )
app.config['UPLOAD_FOLDER'] = AVATAR_UPLOAD_FOLDER

login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/app_users.db")


@login_manager.user_loader
def load_user(user_id):
    # пользователя загрузка с бд
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@login_manager.unauthorized_handler
def unauthorized_callback():
    # Перекинет неавторизованного сюда
    # print(request.path)  # страница, откуда пришли
    # return redirect(f'/login?next={request.path}')
    return redirect(f'/login')


@app.route('/')
@app.route('/about')
def start_page():
    # главная
    # константы
    html = START_PAGE_HTML
    page_title = START_PAGE_TITLE
    # пользователь
    current_user = flask_login.current_user
    is_authenticated = user_is_authenticated(current_user)

    if is_authenticated:
        # если залогинен
        return redirect('/cabinet')

    return render_template(html, page_title=page_title, user=current_user)


@app.route('/registration', methods=["GET", "POST"])
def registration_page():
    # регистрация
    # константы
    page_title = REGISTRATION_PAGE_TITLE
    html = REGISTRATION_PAGE_HTML
    message = ""
    have_errors = False  # ифнормация об ошибках
    avatar_write = False  # записывать ли аватар в бд

    # словарь значений котореы добавляются в класссы инпутов для показания где все верно а где ошбика
    input_errors = get_deepcopy_dict(REGISTRATION_PAGE_INPUT_ERRORS)

    # названия классов для полей ввода
    my_0 = 'my-0'  # my-0 чтоб не было отступа
    is_valid = f"{my_0} {IS_VALID}"  # если прошла проверку
    is_invalid = IS_INVALID  # иначе

    next_page = request.args.get('next')  # куда потом перенаправить

    reg_form = RegisterForm()

    # проверка авторизации
    current_user = flask_login.current_user
    is_authenticated = user_is_authenticated(current_user)

    if reg_form.validate_on_submit():
        # кнопка зарегистрироваться
        # данные из полей
        email = reg_form.email.data.lower()
        username = reg_form.username.data
        password = reg_form.password.data
        password_again = reg_form.password_again.data
        main_currency = reg_form.main_currency.data[0]
        timezone = reg_form.timezone.data
        # print(timezone)
        avatar = reg_form.avatar.data
        avatar_filename = ""

        for key in input_errors.keys():
            # проход по всем инпутам и даем им si valid
            if key != "main_currency" and key != "avatar" and key != "timezone":
                # кроме валюты и аватара, чтобы галочка не мешала
                input_errors[key]["errclass"] = is_valid

        db_sess = db_session.create_session()
        user_email = db_sess.query(User).filter(User.email == email).first()
        user_username = db_sess.query(User).filter(User.username == username).first()

        # проверим все формы на валидность
        if password != password_again:
            # если пароли не совпадают
            have_errors = True
            input_form = "password"

            message = "Пароли не совпадают!"

            # красные рамки ПАРОЛЬ и ПОВТОРИТЬ ПАРОЛЬ
            input_errors[input_form]["errclass"] = is_invalid
            input_errors[f"{input_form}_again"]["errclass"] = is_invalid

            # сообщение снизу
            input_errors["password"]["invalid-feedback"] = message
            input_errors[f"{input_form}_again"]["invalid-feedback"] = message

        if avatar:
            if not allowed_avatar(avatar.filename):
                # проверка корректности авы
                have_errors = True
                input_from = "avatar"

                message = "Некорректный файл!"

                # красная рамка AVATAR
                input_errors[input_from]["errclass"] = is_invalid
                input_errors[input_from]["invalid-feedback"] = message

            else:
                # иначе сделать зеленым
                input_from = "avatar"
                input_errors[input_from]["errclass"] = is_valid

        if user_email:
            # проверка на наличие уже зарегистрированного с таким майлом
            have_errors = True
            input_from = "email"

            message = "Пользователь с таким email уже есть!"

            # красная рамка EMAIL
            input_errors[input_from]["errclass"] = is_invalid
            input_errors[input_from]["invalid-feedback"] = message

        if '@' in username:
            have_errors = True
            input_from = "username"

            message = """Знак "@" не быть использован в логине!"""

            # красная рамка USERNAME
            input_errors[input_from]["errclass"] = is_invalid
            input_errors[input_from]["invalid-feedback"] = message

        elif user_username:
            # проверка на наличие пользователя с таким логином
            have_errors = True
            input_form = "username"

            message = "Пользователь с таким логином уже есть!"

            # красная рамка USERNAME
            input_errors[input_form]["errclass"] = is_invalid
            input_errors[input_form]["invalid-feedback"] = message

        if have_errors:
            # если есть ошибки выводим
            return render_template(html, page_title=page_title, form=reg_form, input_errors=input_errors)

        # иначе записываем в бд и редиректим
        user = User(email=email, username=username, main_currency=main_currency, timezone=timezone,
                    modified_date=get_utc_time())
        user.set_password(password)
        user.set_avatar_filename(avatar, avatar.filename)
        db_sess.add(user)
        db_sess.commit()

        # if next_page:
        #     # если пришли с другой страницы
        #     return redirect(f'/login?next={next_page}')

        return redirect('/login')

    if is_authenticated:
        # если залогинен
        # if next_page:
        #     # если с другой страницы пришел
        #     return redirect(next_page)
        return redirect('/cabinet')

    return render_template(html, page_title=page_title, form=reg_form, input_errors=input_errors)


@app.route('/login', methods=["GET", "POST"])
def login_page():
    # авторизация
    page_title = LOGIN_PAGE_TITLE
    html = LOGIN_PAGE_HTML

    # ифнормация об ошибках
    message = ""
    have_errors = False

    # словарь значений котореы добавляются в класссы инпутов для показания где все верно а где ошбика
    input_errors = get_deepcopy_dict(LOGIN_PAGE_INPUT_ERRORS)

    # названия классов для полей ввода
    my_0 = 'my-0'  # my-0 чтоб не было отступа
    is_valid = f"{my_0} {IS_VALID}"  # если прошла проверку
    is_invalid = IS_INVALID  # иначе

    next_page = request.args.get('next')  # куда потом перенаправить

    # если уже залогинен
    current_user = flask_login.current_user
    if current_user.is_authenticated:
        if next_page:
            # если пришли с другой страницы
            return redirect(next_page)

        return redirect('/cabinet')

    log_form = LoginForm()

    if log_form.validate_on_submit():
        # данные из полей
        email = log_form.email.data.lower()
        password = log_form.password.data
        remember_me = log_form.remember_me.data
        # print(remember_me)

        for key in input_errors.keys():
            # проход по всем инпутам и даем им si valid
            if key != "password":
                input_errors[key]["errclass"] = is_valid

        db_sess = db_session.create_session()

        user = db_sess.query(User).filter(User.email == email).first()

        if user:
            if user.check_password(password):
                login_user(user, remember=remember_me)
                return redirect("/registration")

            have_errors = True
            input_form = "password"

            message = "Неверный пароль!"

            input_errors[input_form]["errclass"] = is_invalid

            input_errors["password"]["invalid-feedback"] = message
        else:
            # если не зареган
            have_errors = True
            input_from = "email"

            message = "Пользователь с таким email не найден!"

            input_errors[input_from]["errclass"] = is_invalid
            input_errors[input_from]["invalid-feedback"] = message

        if have_errors:
            # если есть ошибки выводим
            return render_template(html, page_title=page_title, form=log_form, input_errors=input_errors)
        # # иначе записываем в бд и редиректим
        # user = User(email=email, username=username)
        # user.set_password(log_form.password.data)
        # db_sess.add(user)
        # db_sess.commit()

        return redirect('/cabinet')

    return render_template(html, page_title=page_title, form=log_form, input_errors=input_errors)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route('/cabinet')
@login_required
def cabinet_menu_page():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')

    page_title = "Главная"
    message = ""
    html = "cabinet_page.html"
    have_errors = False
    avatar_path = get_avatar_from_db(current_user)
    sidebar_elements = get_deepcopy_dict(CABINET_PAGE_SIDEBAR_ELEMENTS)  # полная копия

    set_sidebar_a_active_class(sidebar_elements, page_title)  # устновить синим

    return render_template(html, page_title=page_title, user=current_user.username, avatar_path=avatar_path,
                           sidebar_elements=sidebar_elements)
    # return redirect('/login')


@app.route('/cabinet/wallets', methods=["GET", "POST"])
@login_required
def cabinet_wallets_page():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')

    page_title = "Счета"
    message = ""
    html = "cabinet_wallets_page.html"
    have_errors = False

    my_0 = "my-0"
    is_valid = f"{my_0} {IS_VALID}"  # если прошла проверку
    is_invalid = IS_INVALID  # иначе

    avatar_path = get_avatar_from_db(current_user)
    sidebar_elements = get_deepcopy_dict(CABINET_PAGE_SIDEBAR_ELEMENTS)  # полная копия

    set_sidebar_a_active_class(sidebar_elements, page_title)  # устновить синим

    add_wallet_form = AddWalletForm()
    input_errors = get_deepcopy_dict(CABINET_WALLETS_PAGE_ADD_WALLET_MODAL_INPUT_ERRORS)
    wallets_list = get_wallets_list(Wallet, current_user)

    if add_wallet_form.validate_on_submit():
        #  при нажатии кнопки создать

        wallet_name = add_wallet_form.name.data
        balance = add_wallet_form.balance.data
        main_currency = add_wallet_form.main_currency.data[0]
        wallet_color = request.form.get('walletcolor')
        # print(wallet_name, balance, main_currency)

        # if not str(balance).isdigit():
        #     have_errors = True
        #     input_form = "balance"
        #
        #     message = "Могут быть использованы только цифры!"
        #
        #     # красная рамка
        #     input_errors[input_form]["errclass"] = is_invalid
        #     input_errors[input_form]["invalid-feedback"] = message
        #
        db_sess = db_session.create_session()
        wallet = db_sess.query(Wallet).filter(
            Wallet.wallet_name == wallet_name, Wallet.user_id == current_user.id).first()
        if wallet:
            wallet_name = new_wallet_name(Wallet, current_user, wallet_name)
        #
        # if wallet:
        #     print(1)
        #     have_errors = True
        #     input_form = "name"
        #
        #     message = "Кошелёк с таким именем уже есть!"
        #
        #     # красная рамка
        #     input_errors[input_form]["errclass"] = is_invalid
        #     input_errors[input_form]["invalid-feedback"] = message
        #
        # if have_errors:
        #     return render_template(html, page_title=page_title, user=current_user.username,
        #                            avatar_path=avatar_path,
        #                            sidebar_elements=sidebar_elements,
        #                            form=add_wallet_form, input_errors=input_errors,
        #                            wallets=wallets_list)

        try:
            db_sess = db_session.create_session()
            wallet = Wallet(user_id=current_user.id,
                            wallet_name=wallet_name,
                            balance=balance,
                            main_currency=main_currency,
                            wallet_color=get_wallet_color(wallet_color))
            db_sess.add(wallet)
            db_sess.commit()
        except Exception as e:
            print(e)
            print("some problems with add wallet")

        return redirect('/cabinet/wallets')

    return render_template(html, page_title=page_title, user=current_user.username, avatar_path=avatar_path,
                           sidebar_elements=sidebar_elements, form=add_wallet_form, input_errors=input_errors,
                           wallets=wallets_list)


@app.route('/cabinet/transactions', methods=["GET", "POST"])
@login_required
def cabinet_transactions_page():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')

    page_title = "Операции"
    message = ""
    html = "cabinet_transactions_page.html"
    have_errors = False
    avatar_path = get_avatar_from_db(current_user)
    sidebar_elements = get_deepcopy_dict(CABINET_PAGE_SIDEBAR_ELEMENTS)  # полная копия

    set_sidebar_a_active_class(sidebar_elements, page_title)  # устновить синим

    input_errors = CABINET_TRANSACTIONS_PAGE_ADD_TRANSACTION_MODAL_INPUT_ERRORS  # ошибки

    add_transaction_expenses_form = AddTransactionExpensesForm()  # форма расходов
    add_transaction_income_form = AddTransactionIncomeForm()  # форм доходов

    wallets_list = get_wallets_list(Wallet, current_user)  # список счетов
    wallets_names = get_wallets_names(wallets_list)  # список названий кошельков

    add_transaction_expenses_form.wallet.choices = wallets_names  # установить choices для wallet в форму
    add_transaction_income_form.wallet.choices = wallets_names

    get_transactions_list(Transaction, current_user)

    if add_transaction_expenses_form.validate_on_submit():
        #  при нажатии кнопки добавить расход
        transaction_type = "expenses"

        transaction_sum = add_transaction_expenses_form.transaction_sum.data
        wallet = add_transaction_expenses_form.wallet.data
        currency = wallet[-2]
        comment = add_transaction_expenses_form.comment.data
        transaction_category = add_transaction_expenses_form.transaction_expenses_category.data
        transaction_date = add_transaction_expenses_form.transaction_date.data  # время местное

        wallet_id = get_wallet_id_by_name(wallet[:-4], wallets_list)  # получим id кошелька по названию,
        # -4, чтобы не включалась валютва

        try:
            db_sess = db_session.create_session()
            transaction = Transaction(user_id=current_user.id, transaction_type=transaction_type,
                            wallet_id=wallet_id, transaction_sum=transaction_sum, currency=currency,
                            transaction_category=transaction_category,
                            transaction_date=transaction_date, comment=comment)
            db_sess.add(transaction)
            db_sess.commit()

        except Exception as e:
            print(e)
            print("some problems with add transaction expenses")

        try:
            deduct_money_from_wallet(Wallet, current_user, wallet_id, transaction_sum)
        except Exception as e:
            print(e)
            print("some problems with deduct money")

        return redirect('/cabinet/transactions')

    elif add_transaction_income_form.validate_on_submit():
        #  при нажатии кнопки добавить расход
        transaction_type = "income"

        transaction_sum = add_transaction_income_form.transaction_sum.data
        wallet = add_transaction_income_form.wallet.data
        currency = wallet[-2]
        comment = add_transaction_income_form.comment.data
        transaction_category = add_transaction_income_form.transaction_income_category.data
        transaction_date = add_transaction_income_form.transaction_date.data

        wallet_id = get_wallet_id_by_name(wallet[:-4], wallets_list)  # получим id кошелька по названию,
        # -4, чтобы не включалась валютва

        try:
            db_sess = db_session.create_session()
            transaction = Transaction(user_id=current_user.id, transaction_type=transaction_type,
                            wallet_id=wallet_id, transaction_sum=transaction_sum, currency=currency,
                            transaction_category=transaction_category,
                            transaction_date=transaction_date, comment=comment)
            db_sess.add(transaction)
            db_sess.commit()
        except Exception as e:
            print(e)
            print("some problems with add transaction income")

        try:
            add_money_to_wallet(Wallet, current_user, wallet_id, transaction_sum)
        except Exception as e:
            print(e)
            print("some problems with deduct money")

        return redirect('/cabinet/transactions')

    return render_template(html, page_title=page_title, user=current_user.username, avatar_path=avatar_path,
                           sidebar_elements=sidebar_elements, expenses_form=add_transaction_expenses_form,
                           income_form=add_transaction_income_form, input_errors=input_errors,
                           wallets_names=wallets_names, max_time=get_transaction_max_time())


@app.route('/cabinet/income')
@login_required
def cabinet_income_page():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')

    page_title = "Доходы"
    message = ""
    html = "cabinet_income_page.html"
    have_errors = False
    avatar_path = get_avatar_from_db(current_user)
    sidebar_elements = get_deepcopy_dict(CABINET_PAGE_SIDEBAR_ELEMENTS)  # полная копия

    set_sidebar_a_active_class(sidebar_elements, page_title)  # устновить синим

    return render_template(html, page_title=page_title, user=current_user.username, avatar_path=avatar_path,
                           sidebar_elements=sidebar_elements)


@app.route('/cabinet/expenses')
@login_required
def cabinet_expenses_page():
    current_user = flask_login.current_user
    if not current_user.is_authenticated:
        return redirect('/login')

    page_title = "Расходы"
    message = ""
    html = "cabinet_expenses_page.html"
    have_errors = False
    avatar_path = get_avatar_from_db(current_user)
    sidebar_elements = get_deepcopy_dict(CABINET_PAGE_SIDEBAR_ELEMENTS)  # полная копия

    set_sidebar_a_active_class(sidebar_elements, page_title)  # устновить синим

    return render_template(html, page_title=page_title, user=current_user.username, avatar_path=avatar_path,
                           sidebar_elements=sidebar_elements)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1', debug=True)