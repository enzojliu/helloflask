# 代码清单 1-1 hello/app.py： 最小的Flask程序
import click
from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello, Enzo!</h1>'

# 代码清单 1-2 hello/app.py： 绑定多个URL到同一视图函数

@app.route('/hi')
@app.route('/hello')
def say_hello():
    return '<h1>Hello, Flask!</h1>'

# 代码清单 1-3 hello/app.py： 添加URL变量
# 为 greet 视图新添加了一个 app. route() 装饰器，为/greet 设置了默认的 name 值：

@app.route('/greet', defaults={'name': 'Programmer'})
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name

# 上面的用法实际效果等同于：

@app.route('/greet')
@app.route('/greet/<name>')
def greet(name='Programmer'):
    return '<h1>Hello, %s!</h1>' % name

# 代码清单 1-4 hello/app.py： 创建自定义命令

@app.cli.command()
def hello():
    click.echo('Hello, Human!')