from flask_bcrypt import Bcrypt
from app.utils.graph_manager import *
from app.utils.graph_view import *
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, session, Response
from app.services.link import Link

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'



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
        # Check if the username already existsnodes=graph_manager.nodes.values(), graph_data=graphdata
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
    response = None

    if request.method == 'POST':
        node_id = len(graph_manager.nodes) + 1
        content = request.form['content']

        new_node = Node(node_id, content, type='task')
        graph_manager.add_node(new_node)

        # Get the graph data
        graphdata = graph_view_instance.get_graph_data()

        output = ""
        for data in graphdata['nodes']:
            output += f'<li class="p-5 rounded-md shadow-sm border border-slate-100">{data["id"]}. {data["content"]} </li>'

        # Return data as JSON
        json_data = jsonify(graphdata)
        response = Response(
            f'<ul class="space-y-5 py-5" id="tasks" data-nodes="{graphdata["nodes"]}" data-links="{graphdata["links"]}"> <span>{output}</span> <button class="rounded-full p-5 border bg-slate-300">edit</ul>')
        # Set response Header
        response.headers['HX-Trigger'] = 'generateGraph'
    return response


@app.route('/form_graph/<id>', methods=['POST'])
def form_graph(id):
    graph_manager = GraphManager(user_id=session['username'])
    if request.method == 'POST':
        id = int(id)  # Convert id to integer
        content = request.form['content']
        graph_manager.update_node(id, content)
        return 'Content updated'  # Return a simple response indicating success


@app.route('/htmxGetAllTasks', methods=['GET'])
def getAllTasks():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
    #Parse the Json string into aa dictionary
    # graphdata_dict = json.loads(graphdata)
    output = ""
    for data in graphdata['nodes']:
        output +=  f'<li class="p-5 rounded-md shadow-sm border border-slate-100">{data["id"]}. {data["content"]} </li>'
        
    # Return data as JSON
    # json_data = jsonify(graphdata)
    return f' <ul class="space-y-5 py-5" id="tasks" hx-get="/graph_data" hx-target="graph-container">{output}</ul> '

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
    graphdata = graph_view_instance.get_graph_data()
    # Return the graph data as JSON

    return f'<svg class="border w-full h-full" onload="generateGraph({graphdata["nodes"]},{graphdata["links"]});"></svg>'

@app.route('/link/<node_id>/<target_id>', methods=['POST'])
def link(node_id, target_id):
    graph_manager = GraphManager(user_id=session['username'])
    graph_manager.add_link(node_id, target_id)
    return 'Linked hai guys'

@app.route('/delete_node/<node_id>', methods=['POST'])
def delete(node_id):
    graph_manager = GraphManager(user_id=session['username'])
    graph_manager.delete_node(node_id)


if __name__ == '__main__':
    app.run(debug=True)
