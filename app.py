from app.services.node import *
from app.utils.graph_manager import *
from app.utils.graph_view import *
from flask import Flask, render_template, request, redirect, url_for
from flask import jsonify

app = Flask(__name__, template_folder='app/templates')
graph_manager = GraphManager()

graph_view_instance = GraphView(graph_manager)


@app.route('/')
def index():
    # Get the graph data
    graphdata = graph_view_instance.get_graph_data()
    # Render the index template with both nodes and graph data
    return render_template('index.html', nodes=graph_manager.nodes.values(), graph_data=graphdata)


@app.route('/form', methods=['POST'])
def form():
    if request.method == 'POST':
        node_id = len(graph_manager.nodes) + 1
        content = request.form['content']
        tag = request.form['tag']

        new_node = Node(node_id, content, tag)
        graph_manager.add_node(new_node)

        # Return data as JSON
        return jsonify(node_id=node_id, content=content, tag=tag)

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
