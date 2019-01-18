# 代码清单2-1  获取请求URL中的查询字符串

from flask import Flask, request, redirect, url_for, abort, make_response

app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')  # 获取查询参数name的值
    return '<h1>Hello, %s!<h1>' % name  # 插入到返回值中

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