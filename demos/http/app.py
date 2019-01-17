# 代码清单2-1  获取请求URL中的查询字符串

from flask import Flask, request

app = Flask(__name__)

@app.route('/hello')
def hello():
    name = request.args.get('name', 'Flask')  # 获取查询参数name的值
    return '<h1>Hello, %s!<h1>' % name  # 插入到返回值中