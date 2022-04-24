import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import orm
from constants import *
from func_app import *
import os


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    username = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    avatar_filename = sqlalchemy.Column(sqlalchemy.String, default="default.jpg")
    main_currency = sqlalchemy.Column(sqlalchemy.String, default="rub")
    timezone = sqlalchemy.Column(sqlalchemy.String, default="UTC +3")
    hashed_password = sqlalchemy.Column(sqlalchemy.String)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def set_avatar_filename(self, avatar, *avatar_filename):
        filename = AVATAR_FILENAME_DEFAULT  # по умолчанию дефаулт
        if all(avatar_filename):  # если отправили файл
            filename = create_random_filename(avatar_filename[0])  # рандом имя
            try:
                # сохраним фото
                save_image(avatar, AVATAR_UPLOAD_FOLDER, filename)
            except:
                print("problems w save image")
        self.avatar_filename = filename  # даем рандом имя

