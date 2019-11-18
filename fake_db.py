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
from models import User

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# 必须要在context上下文环境中才能单独调用
with app.app_context():
    # 生成随机用户信息
    fake = Faker('zh_CN')
    for i in range(0, 20):
        user = User(username=fake.name(), tel=fake.phone_number(), password=fake.password(6))
        db.session.add(user)
        db.session.commit()
