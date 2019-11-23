"""
@File        : models.py
@Description : ORM数据模型
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from datetime import datetime

from exts import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tel = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, nullable=False)

    @property
    def serialize(self):
        """
        转json格式用
        :return:
        """
        return {
            'id': self.id,
            'tel': self.tel,
            'password': self.password,
            'username': self.username
        }


class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 这里注意不能用now()，否则会导致时间不自动更新（一直停留在程序启动的时间点）
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    author = db.relationship('User', backref=db.backref('article'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), default=0)
    category = db.relationship('Categories', backref=db.backref('articles'))

    @property
    def serialize(self):
        """
        转json格式用
        :return:
        """
        return {
            'id': self.id,
            'title': self.title,
            # 'content': self.content,
            'create_time': self.create_time,
            'author_name': self.author.username,
            'category_name': self.category.name
        }


class Categories(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
