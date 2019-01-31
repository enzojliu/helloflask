from flask import Flask, render_template, flash, redirect, url_for, request

from forms import LoginForm

app = Flask(__name__)

app.secret_key = 'secret string'
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/html', methods=['GET', 'POST'])
def html():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form.get('username')
        flash('Welcome home, %s' % username)
        return redirect(url_for('index'))
    return render_template('pure_html.html')


app.route('/basic')
def basic():
    form = LoginForm()
    return render_template('login.html', form=form)