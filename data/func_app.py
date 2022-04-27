import flask_login
from constants import *
import os
import random
import string
import cv2
from copy import deepcopy
from data import db_session
import random
import pytz
from datetime import datetime, timedelta


def user_is_authenticated(current_user):
    if current_user.is_authenticated:
        return True
    return False


def allowed_avatar(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in AVATAR_ALLOWED_EXTENSIONS


def save_image(image, upload_folder, filename):
    image.save(os.path.join(upload_folder, filename))


def create_random_filename(filename, name_len=8):
    try:
        file_extension = '.' + filename.rsplit('.', 1)[1].lower()
        s = string.ascii_lowercase + string.ascii_uppercase + string.digits
        filename = ''.join(random.sample(s, name_len)) + file_extension
        # filename = r"default.jpg"
        path_to_file = os.path.join(AVATAR_UPLOAD_FOLDER, filename)
        while os.path.isfile(path_to_file):
            filename = ''.join(random.sample(s, name_len)) + file_extension
            path_to_file = os.path.join(AVATAR_UPLOAD_FOLDER, filename)
    except Exception as e:
        print("some problems with create_random_name")
        print(e)
        filename = "default.jpg"

    return filename


def get_avatar_from_db(current_user):
    try:
        avatar_filename = current_user.avatar_filename
    except:
        avatar_filename = AVATAR_FILENAME_DEFAULT

    avatar_path = f"{AVATARS_UPLOAD_URL_FOR_FOLDER}/{avatar_filename}"

    return (avatar_path)


def get_deepcopy_dict(dict_):
    # вернет копию словаря
    return deepcopy(dict_)


def set_sidebar_a_active_class(dict_, elem_title):
    # поставить класс актив к элементу сайдбара a
    try:
        for key in dict_.keys():
            if key == elem_title:
                dict_[key]["a_class"] = f"""{dict_[key]["a_class"]} active"""
                return dict_
    except Exception as e:
        print(f"error with set a active class")
        return dict_


def get_wallets_list(Wallet, current_user):
    wallets_list = []
    try:
        db_sess = db_session.create_session()
        wallets = db_sess.query(Wallet).filter(Wallet.user_id == current_user.id).all()
        for elem in wallets:
            # print(el.wallet_name, el.balance)
            wallets_list.append(
                {
                    "name": elem.wallet_name,
                    "id": elem.id,
                    "balance": beautiful_balance(elem.balance),
                    "currency": elem.main_currency[0],
                    "wallet_color": elem.wallet_color
                }
            )
        return wallets_list
    except Exception as e:
        print(e)
        print("some problems with get wallets list")


def get_wallets_names(wallets_list):
    arr = []
    try:
        for el in wallets_list:
            # arr.append(el["name"])
            arr.append(f"""{el["name"]} ({el["currency"][0]})""")
        return arr
    except:
        print("some problems  with get wallets_list")


def get_wallet_id_by_name(wallet_name, wallets_list):
    for wallet in wallets_list:
        if wallet["name"] == wallet_name:
            return wallet["id"]
    return None


def new_wallet_name(Wallet, current_user, wallet_name):
    wallet_name_def = wallet_name
    db_sess = db_session.create_session()
    wallet = db_sess.query(Wallet).filter(
        Wallet.wallet_name == wallet_name, Wallet.user_id == current_user.id).first()
    i = 2
    while wallet and i < 30:
        wallet_name = f"{wallet_name_def} ({i})"
        i += 1
        wallet = db_sess.query(Wallet).filter(
            Wallet.wallet_name == wallet_name, Wallet.user_id == current_user.id).first()
    if i >= 30:
        s = string.ascii_lowercase + string.ascii_uppercase + string.digits
        name_len = 8
        wallet_name = ''.join(random.sample(s, name_len))
    return wallet_name


def beautiful_balance(balance):
    balance = str(balance)
    s = list(balance)
    for i in range(len(balance), 0, -3):
        s.insert(i, ' ')
    s = ''.join(s)
    return s


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))
    return r, g, b


def rgb_to_hex(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)


def muted_color(r, g, b):
    # менее контрастный цвет
    # r, g, b = max(min(255, 180 + r // 255), r), max(min(255, 180 + g // 255), g), max(min(255, 180 + b // 255), b)
    return r, g, b


def get_random_wallet_color():
    r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    r, g, b = muted_color(r, g, b)
    return r, g, b


def get_wallet_color(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    r, g, b = muted_color(r, g, b)
    hex_color = rgb_to_hex(r, g, b)
    return hex_color


def deduct_money_from_wallet(Wallet, current_user, wallet_id, expense_sum):
    db_sess = db_session.create_session()
    wallet = db_sess.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == current_user.id).first()
    wallet.balance -= expense_sum
    db_sess.commit()


def add_money_to_wallet(Wallet, current_user, wallet_id, expense_sum):
    db_sess = db_session.create_session()
    wallet = db_sess.query(Wallet).filter(Wallet.id == wallet_id, Wallet.user_id == current_user.id).first()
    wallet.balance += expense_sum
    db_sess.commit()


def get_utc_time():
    # получить время по гринвичу
    try:
        utc_time = pytz.utc
        datetime_utc = datetime.now(utc_time)
        # datetime_utc = datetime.now(utc_time).strftime("%Y-%m-%d %H:%M:%S")
        # print(datetime_utc)
        return datetime_utc
    except:
        print("some problems with get utc time")
        return datetime.now()


def get_current_time(timezone="+0"):
    try:
        return get_utc_time() + timedelta(hours=int(timezone[-2:]))
    except:
        print("some problems with get current time")
        return get_utc_time()


def get_transaction_max_time(timezone="+3"):
    max_time = get_utc_time() + timedelta(hours=int(timezone[-2:]))
    return max_time.strftime("%Y-%m-%dT%H:%M:%S")


def get_transactions_list(Transaction, current_user):
    # сначала найдем последнюю дату
    transactions_dict = {}
    db_sess = db_session.create_session()
    transactions_by_date_list = db_sess.query(Transaction).filter(
        Transaction.user_id == current_user.id).order_by(Transaction.transaction_date).all()
    transactions_by_date_list = transactions_by_date_list[::-1]
    try:
        transaction = transactions_by_date_list[0]
        date = transaction.transaction_date.strftime("%Y-%m-%d")
        print(date)

        transactions_dict[date] = [
                    {
                        "id": transaction.id,
                        "user_id": transaction.user_id,
                        "wallet_id": transaction.wallet_id,
                        "type": transaction.transaction_type,
                        "category": transaction.transaction_category,
                        "sum": transaction.transaction_sum,
                        "currency": transaction.currency,
                        "comment": transaction.comment
                    }
        ]
        for transaction in transactions_by_date_list[1:]:
            if transaction.transaction_date.strftime("%Y-%m-%d") == date:
                transactions_dict[date].append(
                    {
                        "id": transaction.id,
                        "user_id": transaction.user_id,
                        "wallet_id": transaction.wallet_id,
                        "type": transaction.transaction_type,
                        "category": transaction.transaction_category,
                        "sum": transaction.transaction_sum,
                        "currency": transaction.currency,
                        "comment": transaction.comment
                    })
            else:
                date = transaction.transaction_date.strftime("%Y-%m-%d")

                transactions_dict[date] = [
                    {
                        "id": transaction.id,
                        "user_id": transaction.user_id,
                        "wallet_id": transaction.wallet_id,
                        "type": transaction.transaction_type,
                        "category": transaction.transaction_category,
                        "sum": transaction.transaction_sum,
                        "currency": transaction.currency,
                        "comment": transaction.comment
                    }
                ]
        print(transactions_dict)
    except Exception as e:
        print(e)
        print("some problemswith get transa list")










