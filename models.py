from datetime import datetime

from exts import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tel = db.Column(db.String(11), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), nullable=False)


class Article(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime, default=datetime.now)  # 这里注意不能用now()，否则会导致时间不自动更新（一直停留在程序启动的时间点）
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', backref=db.backref('question'))
