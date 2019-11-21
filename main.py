"""
@File        : main.py
@Description : 应用主入口
@Time        : 2019/11/19 0:57
@Author      : DexterLien
@Email       : lpwm@qq.com
@Software    : PyCharm
"""
from flask import Flask, render_template, request, session, redirect, url_for, g, jsonify

import config
from decorators import login_check
from models import *

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    """
    首页
    :return:
    """
    # 获取当前页码
    page = request.args.get(key='page', default=1, type=int)
    # 实现分页
    pagination = Article.query.order_by(
        Article.create_time.desc()).paginate(page, per_page=5, error_out=False)
    content = {
        # 这里需要注意使用text('-create_time')作为排序的参数传入,和教程中不太一样
        # 貌似是版本不一样,试了下去掉-的话不需要加text()
        # 'articles': Article.query.order_by(text('-create_time')).all(),
        # 返回分页后的文章对象
        'articles': pagination.items,
        'pagination': pagination
    }
    return render_template('index.html', **content)


@app.route('/profile')
def profile():
    """
    用户个人中心
    :return:
    """
    return render_template('profile.html', user=g.user)


@app.route('/detail/<article_id>')
def detail(article_id):
    """
    详情页面
    :return:
    """
    detail_article = Article.query.filter(Article.id == article_id).first()
    return render_template('detail.html', article=detail_article)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    注册
    :return:
    """
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        tel = request.form.get('tel')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        username = request.form.get('username')
        user = User.query.filter(User.tel == tel).first()
        if user:
            return u'该手机号已被注册,请更换手机号码'
        if password1 != password2:
            return '两次输入密码不一致,请检查重新输入'
        else:
            user = User(tel=tel, username=username, password=password1)
            db.session.add(user)
            db.session.commit()
            return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    登录
    :return:
    """
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        tel = request.form.get('tel')
        password = request.form.get('password')
        user = User.query.filter(User.tel == tel, User.password == password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return '登陆失败'


@app.route('/logout')
def logout():
    """
    注销
    :return:
    """
    session.clear()
    return redirect(url_for('index'))


@app.route('/add', methods=['GET', 'POST'])
@login_check
def add():
    """
    添加文章
    :return:
    """
    if request.method == 'GET':
        return render_template('add.html')
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        article = Article(title=title, content=content)
        article.author = g.user

        db.session.add(article)
        db.session.commit()
        result = {'message': '文章提交成功', 'status': 'ok'}
        return jsonify(result)


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """
    后台管理
    :return:
    """
    if request.method == 'GET':
        return render_template('admin/index.html')


@app.route('/admin/category', methods=['GET', 'POST'])
def admin_category():
    """
    栏目管理
    :return:
    """
    if request.method == 'GET':
        return render_template('admin/category.html')
    if request.method == 'POST':
        return render_template('admin/category.html')


@app.route('/admin/users', methods=['GET', 'POST'])
def admin_users():
    """
    用户管理
    :return:
    """
    if request.method == 'GET':
        return render_template('admin/users.html')

    if request.method == 'POST':
        method = request.form.get('method')
        # 添加
        if method == 'add':
            f = request.form
            user = User(username=f.get('username'), tel=f.get('tel'), password=f.get('password'))
            db.session.add(user)
            db.session.commit()
            return jsonify({
                'code': 0,
                'msg': '用户创建成功!'
            })
        # 删除
        if method == 'delete':
            user_id = request.form.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            if user:
                db.session.delete(user)
                db.session.commit()
                return jsonify({
                    'status': 0,
                    'msg': '用户删除成功!'
                })
            else:
                return jsonify({
                    'status': -1,
                    'msg': '用户删除失败,请联系管理员.'
                })
        # 查询
        if method == 'query':
            tel = request.form.get('tel')
            user = User.query.filter(User.tel == tel).first()
            if user:
                users = [user.serialize]
                return jsonify({
                    'code': 0,
                    'data': users
                })
            else:
                return jsonify({
                    'code': -1,
                    'msg': '没有找到用户'
                })
        # 重置密码
        if method == 'reset':
            user_id = request.form.get('user_id')
            user = User.query.filter(User.id == user_id).first()
            if user:
                user.password = '123456'
                db.session.commit()
                return jsonify({
                    'status': 0,
                    'msg': user.username + '密码已重置为123456'
                })
            else:
                return jsonify({
                    'status': -1,
                    'msg': '密码重置失败,请联系管理员.'
                })
        # 分页获取
        if method == 'paginate':
            page = request.form.get(key='page', default=1, type=int)
            limit = request.form.get(key='limit', default=10, type=int)
            pagination = User.query.paginate(page, per_page=limit, error_out=False)

            users = pagination.items
            users = [i.serialize for i in users]
            total_count = User.query.count()  # 获取全部user表中的记录数量
            result = {
                'code': 0,
                'msg': '',
                'count': total_count,  # 这个是全部数据集的数量,不是分页的单页数量
                'data': users
            }
            return jsonify(result)


@app.before_request
def before_request():
    """
    每次请求前执行的钩子函数,校验用户是否登录
    如果已经登录,将用户对象存入全局变量g中
    """
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def check_login_user_processor():
    """
    每次获取上下文(调用模板渲染的时候)的钩子函数,如果用户已登录,将用户对象注入给模板变量
    :return:
    """
    if hasattr(g, 'user'):
        return {'user': g.user}
    # return {'user': 'Dexter'}
    return {}


if __name__ == '__main__':
    app.run()
