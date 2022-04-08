import flask_login


def user_is_authenticated(current_user):
    if current_user.is_authenticated:
        return True
    return False

