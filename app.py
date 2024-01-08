from flask import render_template
from app.models.node import *
from app.utils.graph_manager import *
from flask import Flask, jsonify, request

app = Flask(__name__)
graph_manager = GraphManager()  # Instantiate your GraphManager


app = Flask(__name__)
nodes = {}

@app.route('/')
def home():
    return render_template('index.html') 

@app.route('/nodes', methods=['POST'])
def create_node():
    data = request.json
    node = Node(id=data['id'], content=data['content'], links=[], metadata=data['metadata'])
    try:
        graph_manager.add_node(node)
    except ValueError as e:
        return jsonify({'message': str(e)}), 400
    return jsonify(node.id), 201

@app.route('/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    node = graph_manager.find_node(node_id)
    if not node:
        return jsonify({'message': 'Node not found'}), 404
    # Assuming Node has a method to convert itself to a dict for JSON response
    return jsonify(node.to_dict()), 200

# Additional routes to update and delete nodes using graph_manager would be here...

if __name__ == '__main__':
    app.run(debug=True)
