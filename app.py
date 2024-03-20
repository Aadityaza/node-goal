from flask_bcrypt import Bcrypt
from app.utils.graph_manager import *
from app.utils.graph_view import *
import app.utils.search as search
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify, session, Response
from app.services.link import Link
from app.services.user import *
import ulid
import networkx as nx


app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
bcrypt = Bcrypt(app)
app.secret_key = 'your_secret_key'




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    users = load_users()

    if username in users and bcrypt.check_password_hash(users[username], password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        return 'Invalid username or password <button @click="login = true" class="bg-neutral-400 hover:bg-neutral-300 px-4 py-2 text-neutral-900 rounded-md w-fit" >Back to Login</button> '


@app.route('/register', methods=['POST'])
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
@app.route('/username-validation', methods=['POST'])
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

@app.route('/user-password-validation', methods=['POST'])
def userPasswordValidation():
    password = request.form['password']
    if len(password) < 8:
        return 'password cannot be less then 8 characters'
    return ""
# Register Form Validation Ends ------------------------------


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

def map_score_to_radius(score, min_radius, max_radius):
    # Ensure score is within bounds
    score = max(0, min(1, score))
    
    # Calculate radius using linear interpolation
    radius = min_radius + (max_radius - min_radius) * score
    
    return radius

def map_score_to_radius(score, min_radius, max_radius):
    # Ensure score is within bounds
    score = max(0, min(1, score))
    
    # Calculate radius using linear interpolation
    radius = min_radius + (max_radius - min_radius) * score
    
    return radius

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
    # Render the index template with both nodes and graph data
  
    G = nx.DiGraph()
    for data in graphdata['nodes']:
        G.add_node(data['id'])
    for link in graphdata['links']:
        G.add_edge(link['source'], link['target'])

    pagerank_scores = nx.pagerank(G)
    min_radius = 3
    max_radius = 30

    radius_dict = {}

    for key, score in pagerank_scores.items():
        radius = map_score_to_radius(score, min_radius, max_radius)
        radius_dict[key] = str(radius)

    return render_template('dashboard.html', nodes=graph_manager.nodes.values(), graph_data=graphdata ,radius_dict=radius_dict)

# Please Migrate all those functions wrapped with HTMX to it's own .py file
#---------- HTMX ------------# 
@app.route('/form', methods=['POST'])
def form():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    response = None

    if request.method == 'POST':
        desired_length = 15
        node_id = str(ulid.new().int)[:desired_length]  # Generate a ULID
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
@app.route('/link/<node_id>/<target_id>', methods=['GET'])
def link(node_id, target_id):
    graph_manager = GraphManager(user_id=session['username'])
    graph_manager.add_link(node_id, target_id)
    return 'Linked hai guys'
#---------- HTMX ------------# 


@app.route('/search/<node_id>',methods=['GET', 'POST'])
def searchResult(node_id):
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    word = request.form['search']
    # Get graph data for the frontend from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    matches= search.match(word,graph_data,node_id)
    print(matches)
    return render_template('/htmx/searchResults.html',matches=matches ,node_id=node_id) 

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

@app.route('/node_importance')
def data():
    graph_manager = GraphManager(user_id=session['username'])
    graph_view_instance = GraphView(graph_manager)
    # Get the graph data
    data = graph_view_instance.get_graph_data()
    G = nx.DiGraph()
    for node_data in data['nodes']:
        G.add_node(node_data['id'])
    for link in data['links']:
        G.add_edge(link['source'], link['target'])
    pagerank_scores = nx.pagerank(G)
    return pagerank_scores



if __name__ == '__main__':
    app.run(debug=True)
