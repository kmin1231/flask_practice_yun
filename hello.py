from flask import Flask, render_template, redirect, url_for, abort

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/index')
@app.route('/')
def hello_world():
    return 'Hello, world!'

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass
    if request.method == 'POST':
        # reutrn do_the_login()
        pass
    else:
        # return show_the_login_form()
        pass

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['TEMPLATES_AUTO_RELOAD'] = True