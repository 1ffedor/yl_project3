import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm
from constants import *
from func_app import *
import os


class Transaction(SqlAlchemyBase, UserMixin):
    __tablename__ = 'transactions'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    wallet_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("wallets.id"))
    transaction_sum = sqlalchemy.Column(sqlalchemy.Integer)
    currency = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)
    user = orm.relation('User')
    wallet = orm.relation('Wallet')

