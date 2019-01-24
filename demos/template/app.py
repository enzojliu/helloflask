from flask import Flask, render_template, Markup, url_for,

app=Flask(__name__)

user = {
    'username': 'Grey Li',
    'bio': 'A boy who loves movies and music.',
}

movies = [
    {'name': 'My Neighbo Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1987'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket List', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'Coco', 'year': '2017'},
]
# render HTML templates
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)

# the main page
@app.route('/')
def index():
    return render_template('index.html')

# 3-3 模板上下文处理函数
@app.context_processor
def inject_foo():
    foo = 'I am foo.'
    return dict(foo=foo)  # 等同于return {'foo': foo}

# register template global function
@app.template_global()
def bar():
    return 'I am bar.'

# 代码清单3-6 　 template/app.py：注册自定义测试器
@app.template_test()
def baz(n):
    if n == 'baz':
        return True
    return False