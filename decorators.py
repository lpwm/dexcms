from functools import wraps
from flask import session, redirect, url_for


def login_check(func):
    """
    校验登录状态
    :param func:
    :return:
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('user_id'):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('login'))

    return wrapper