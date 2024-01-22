from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_bcrypt import Bcrypt
import json
import os

from app.services.node import *
from app.utils.graph_manager import *
from app.utils.graph_view import *
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'  # Change this to a random secret key



class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash


def load_users():
    if not os.path.exists('users.json'):
        return {}
    with open('users.json', 'r') as f:
        users = json.load(f)
    return users


def save_user(user):
    users = load_users()
    users[user.username] = user.password_hash
    with open('users.json', 'w') as f:
        json.dump(users, f)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()

        if username in users and bcrypt.check_password_hash(users[username], password):
            session['username'] = username

            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password', 401

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Load existing users
        users = load_users()

        # Check if the username already exists
        if username in users:
            return 'Username already exists', 400

        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(username, password_hash)
        save_user(new_user)

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
    # Render the index template with both nodes and graph data
    return render_template('dashboard.html', nodes=graph_manager.nodes.values(), graph_data=graphdata)


@app.route('/form', methods=['POST'])
def form():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    if request.method == 'POST':
        node_id = len(graph_manager.nodes) + 1
        content = request.form['content']

        new_node = Node(node_id, content)
        graph_manager.add_node(new_node)

        # Return data as JSON
        return jsonify(node_id=node_id, content=content)


@app.route('/graph')
def graph_view():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    # Get graph data for the frontend from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    # Render the graph template with the graph data
    return render_template('graph.html', graph_data=graph_data)


@app.route('/graph_data')
def graph_data():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    # Get graph data from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    # Return the graph data as JSON
    return jsonify(graph_data)


if __name__ == '__main__':
    app.run(debug=True)
