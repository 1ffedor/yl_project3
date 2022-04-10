import flask_login
from constants import *
import os
import random
import string
import cv2


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
        print("some problems with create_randm_name")
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









