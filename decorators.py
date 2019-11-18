"""
@File        : decorators.py
@Description : 装饰器
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
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
