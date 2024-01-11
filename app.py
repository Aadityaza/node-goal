from app.services.node import *
from app.utils.graph_manager import *
from app.utils.graph_view import *
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import ChoiceLoader, FileSystemLoader
from flask import jsonify


app = Flask(__name__, template_folder='app/templates')
graph_manager = GraphManager()

graph_view_instance = GraphView(graph_manager)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        node_id = len(graph_manager.nodes) + 1  # Or however you generate new IDs
        content = request.form.get('content')
        tag = request.form.get('tag')
        # Assuming GraphManager has an 'add_node' method
        graph_manager.add_node(Node(node_id, content, tag))
        # Redirect to the graph view page after adding the node
        return redirect(url_for('graph_view'))

    # If it's not a POST request, just render the index page
    return render_template('index.html', nodes=graph_manager.nodes.values())

@app.route('/graph')
def graph_view():
    # Get graph data for the frontend from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    # Render the graph template with the graph data
    return render_template('graph.html', graph_data=graph_data)

@app.route('/graph_data')
def graph_data():
    # Get graph data from the GraphView instance
    graph_data = graph_view_instance.get_graph_data()
    # Return the graph data as JSON
    return jsonify(graph_data)


if __name__ == '__main__':
    app.run(debug=True)