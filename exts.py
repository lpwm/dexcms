"""
@File        : exts.py
@Description : 初始化ORM中的db对象,防止循环import
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()
