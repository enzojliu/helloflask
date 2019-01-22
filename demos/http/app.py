import os

from jinja2 import escape
from jinja2.utils import generate_lorem_ipsum
from urllib.parse import urlparse, urljoin
from flask import Flask, request, redirect, url_for, abort, make_response, json, jsonify, session

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'secret string')


@app.route('/')
@app.route('/hello')
def hello():
    name = request.args.get('name')  # 获取查询参数name的值
    if name is None:
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!<h1>' % escape(name)  # escape name to avoid XSS
    # return different response according to the user's authentication status
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

# json
@app.route('/fo')
def fo():
    data = {'name':'Grey Li', 'gender':'male'}
    response = make_response(json.dumps(data))
    response.mimetype = 'application/json'
    return response


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

# redirect to last page
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something', next=request.full_path)

@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something', next=request.full_path)

# do_something
@app.route('/do_something_and_redirect')
def do_something():
    # do something
    return redirect_back()


def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if target:
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

# AJAX
@app.route('/post')
def show_post():
    post_body = generate_lorem_ipsum(n=2)  # 生成两段随机文本
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="load">Load More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url:'/more',       // 目标 URL
            type:'get',        // 请求方法
            success:function(data){           // 返回2XX响应后触发的回调函数
                $('.body').append(data);      // 将返回的响应插入到页面中
            }
        }）
    }）
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)