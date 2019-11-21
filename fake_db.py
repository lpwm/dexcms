"""
@File        : fake_db.py
@Description : 生成随机user数据表内容
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from flask import Flask
import config
from exts import db
from faker import Faker
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
    user = User(username=fake.name(), tel=fake.phone_number(), password=fake.password(6))
    db.session.add(user)
    db.session.commit()


def generate_article():
    """
    生成随机内容文章
    :return:
    """
    title = fake.text(fake.random_int(20, 50))
    content = fake.text(1000)
    create_time = fake.date_time().strftime('%Y-%m-%d %H:%M:%S')
    author_id = fake.random_int(1, 5)
    cate_id = fake.random_int(1, 3)
    article = Article(title=title, content=content, create_time=create_time,
                      author_id=author_id, category_id=cate_id)
    db.session.add(article)
    db.session.commit()


if __name__ == '__main__':
    # 必须要在context上下文环境中才能单独调用
    with app.app_context():
        for i in range(0, 15):
            generate_article()
