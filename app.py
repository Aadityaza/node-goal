from flask_bcrypt import Bcrypt
from app.utils.graph_manager import *
from app.utils.graph_view import *
import app.utils.search as search
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, session, Response
from app.services.link import Link
from app.services.user import *
import ulid

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'




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

# Please Migrate all those functions wrapped with HTMX to it's own .py file
#---------- HTMX ------------# 
@app.route('/form', methods=['POST'])
def form():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    response = None

    if request.method == 'POST':
        node_id = str(ulid.new().int)  # Generate a ULID
        content = request.form['content']

        new_node = Node(int(node_id), content, type='task')  # Use ULID instead of incremental ID
        graph_manager.add_node(new_node)

        # Get the graph data
        graphdata = graph_view_instance.get_graph_data()
    return render_template('/htmx/taskCards.html', nodes=graphdata['nodes'], links=graphdata['links'], hello="hello")#---------- HTMX ------------#
#---------- HTMX ------------#


#---------- HTMX ------------# 
@app.route('/form_graph/<id>', methods=['POST'])
def form_graph(id):
    graph_manager = GraphManager(user_id=session['username'])
    if request.method == 'POST':
        id = int(id)  # Convert id to integer
        content = request.form['content']
        graph_manager.update_node(id, content)
        # This will replace it's respective title
        return content 

#---------- HTMX ------------# 

#---------- HTMX ------------# 
@app.route('/htmxGetAllTasks', methods=['GET'])
def getAllTasks():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
        
    return render_template('/htmx/initialTaskCards.html', nodes=graphdata['nodes'], hello='helloWorld' )
#---------- HTMX ------------# 





#--------- I think this below is not being used, If so you can remove it ----------#
@app.route('/graph')
def graph_view():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    # Get graph data for the frontend from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    # Render the graph template with the graph data
    return render_template('graph.html', graph_data=graph_data)
#--------- I think this above is not being used, If so you can remove it ----------#



#---------- HTMX ------------# 
@app.route('/link/<node_id>/<target_id>', methods=['POST'])
def link(node_id, target_id):
    graph_manager = GraphManager(user_id=session['username'])
    graph_manager.add_link(node_id, target_id)
    return 'Linked hai guys'
#---------- HTMX ------------# 


@app.route('/search/<node_id>/<word>',methods=['GET', 'POST'])
def searchResult(node_id,word):
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)

    # Get graph data for the frontend from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    matches= search.match(word,graph_data,node_id)
    return matches

#---------- HTMX ------------# 
@app.route('/delete_node/<node_id>', methods=['POST'])
def delete(node_id):

    node_id = int(node_id)  # Convert id to integer
    graph_manager = GraphManager(user_id=session['username'])
    graph_manager.delete_node(node_id)
    graph_view_instance = GraphView(graph_manager)
    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
    return render_template('/htmx/taskCards.html', nodes=graphdata['nodes'],links=graphdata['links'])
#---------- HTMX ------------# 



if __name__ == '__main__':
    app.run(debug=True)
