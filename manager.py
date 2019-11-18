"""
@File        : manager.py
@Description : 命令行对数据库进行ORM映射更新
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main import app
from exts import db
from models import User, Article

manager = Manager(app)

# 绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
