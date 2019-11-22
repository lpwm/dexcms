"""
@File        : fake_db.py
@Description : 生成随机user数据表内容
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from faker import Faker
from flask import Flask

import config
from models import *

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
fake: Faker = Faker('zh_CN')


def generate_user():
    """
    生成随机用户信息
    :return:
    """
    user = User(username=fake.name(), tel=fake.phone_number(), password=fake.password(6), role=fake.random_int(1, 2))
    db.session.add(user)
    db.session.commit()


def generate_cate():
    """
    初始化分类信息
    :return:
    """
    db.session.add(Categories(name='学习资料'))
    db.session.add(Categories(name='每周一答'))
    db.session.commit()


def generate_article():
    """
    生成随机内容文章
    :return:
    """
    title = fake.text(fake.random_int(20, 50))
    content = fake.text(1000)
    create_time = fake.date_time().strftime('%Y-%m-%d %H:%M:%S')
    author_id = fake.random_int(1, 2)
    cate_id = fake.random_int(1, 2)
    article = Article(title=title, content=content, create_time=create_time,
                      author_id=author_id, category_id=cate_id)
    db.session.add(article)
    db.session.commit()


if __name__ == '__main__':
    # 必须要在context上下文环境中才能单独调用
    with app.app_context():
        generate_cate()
        for i in range(0, 2):
            generate_user()
        for i in range(0, 15):
            generate_article()
