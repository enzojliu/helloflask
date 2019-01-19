import os
from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')  # 获取查询参数name的值
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!<h1>' % name  # 插入到返回值中
    # 根据 用户 认证 状态 返回 不同 的 内容
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# use int URL converter 使用URL int 转换器
@app.route('/goback/<int:year>')
def go_back(year):
    return '<p>Welcome to %d!</p>' % (2018 - year)


# use any URL converter
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p>Love is patient and kind. Love is not jealous or boastful or proud or rude.</p>'


# redirect
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# return error response
@app.route('/brew/<drink>')
def teapot(drink):
    if drink == 'coffee':
        abort(418)
    else:
        return 'A drop of tea.'


# 404
@app.route('/404')
def not_found():
    abort(404)


# change MIMEtype
@app.route('/foo')
def foo():
    response = make_response('Hello, World')
    response.mimetype = 'type/plain'
    return response


# json
@app.route('/fo')
def fo():
    data = {'name':'Grey Li', 'gender':'male'}
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


# jsonify() 函数
@app.route('/fooo')
def fooo():
    return jsonify(message='Error!'), 500


# set_cookie 代码清单 2-4  http/app.py：设置 cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response

# session
@app.route('/login')
def login():
    session['logged_in'] = True # 写入session
    return redirect(url_for('hello'))


# 代码清单 2-6 　http/app.py：模拟管理后台
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page. '


# 代码清单 2-7 　http/app.py：登出账户
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))