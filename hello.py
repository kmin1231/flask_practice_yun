from flask import Flask, render_template, redirect, url_for, abort
from flask.views import View, MethodView
from mongoengine import connect
from v1 import app as v1_app
from v2 import app as v2_app
from config import FlaskConfig

app = Flask(__name__, static_folder='static', template_folder='templates')
app.register_blueprint(v1_app)
app.register_blueprint(v2_app)

app.config['MONGO_URI'] = FlaskConfig.MONGO_URI

try:
    connect(host=app.config['MONGO_URI'])
    print("MongoDB connection success!")
except:
    print("Failed to connect to MongoDB")

@app.route('/index')
def hello_world():
    return 'Hello, world!'

@app.route('/')
def index():
    return redirect(url_for('user_list'))

@app.route('/hello')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)

@app.route('/users')
def user_list():
    users = []
    return render_template('users.html', users=users)

class UserList(View):
    methods = ['GET', 'POST']

    def dispatch_request(self):
        users = []
        return render_template('users.html', users=users)

class UserView(MethodView):
    def get(self, user_id):
        if user_id is None:
            return 'all'    # return a list of users
        else:
            return 'one'    # expose a single user
    
    def post(self):
        return 'post'
    
    def put(self, user_id):
        return 'put'
    
    def delete(self, user_id):
        return 'delete'

user_view = UserView.as_view('users')
app.add_url_rule('/users', defaults={'user_id': None}, view_func=user_view, methods=['GET'])
app.add_url_rule('/users', view_func=user_view, methods=['POST'])
app.add_url_rule('/users/<int:user_id>', view_func=user_view, methods=['GET', 'PUT', 'DELETE'])

@app.route('/v1/users')
def v1_users():
    return 'v1'

@app.route('/v2/users')
def v2_users():
    return 'v2'

@app.route('/login', methods=['GET', 'POST'])
def login():
    pass
    if request.method == 'POST':
        # reutrn do_the_login()
        pass
    else:
        # return show_the_login_form()
        pass

@app.errorhandler(403)
def permission_denied(error):
    return '403', 403

app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['TEMPLATES_AUTO_RELOAD'] = True