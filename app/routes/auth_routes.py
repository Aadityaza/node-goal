from flask import Flask, request, redirect, url_for
from flask_bcrypt import Bcrypt
from app.services.user import *
from flask import jsonify, session
from flask import Blueprint
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')


auth = Blueprint('auth', __name__, template_folder='templates')
bcrypt = Bcrypt(app)


@auth.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()

    if username in users and bcrypt.check_password_hash(users[username], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid username or password <button @click="login = true" class="bg-neutral-400 hover:bg-neutral-300 px-4 py-2 text-neutral-900 rounded-md w-fit" >Back to Login</button> '


@auth.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # Load existing users
    users = load_users()
    # Check if the username already exists
    if username in users:
        return 'Username already exists  '
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    # Check if the username already existsnodes=graph_manager.nodes.values(), graph_data=graphdata
    new_user = User(username, password_hash)
    save_user(new_user)

    return 'User Created Successfully <button @click="login = true" class="bg-neutral-400 hover:bg-neutral-300 px-4 py-2 text-neutral-900 rounded-md w-fit" >Back to Login</button>' 

# Register form Validation Starts ------------------------------
@auth.route('/username-validation', methods=['POST'])
def userValidation():
    username = request.form['username']
    # Load existing users
    users = load_users()
    if len(username) < 3:
        return 'Username cannot be less then 3 characters'
    # Check if the username already exists
    if username in users:
        return 'Username already exists'

    return ""

@auth.route('/user-password-validation', methods=['POST'])
def userPasswordValidation():
    password = request.form['password']
    if len(password) < 8:
        return 'password cannot be less then 8 characters'
    return ""
# Register Form Validation Ends ------------------------------


@auth.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
