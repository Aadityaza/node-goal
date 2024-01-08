from flask import Blueprint, request, jsonify
from app.utils.graph_manager import GraphManager
from app.models.node import Node

graph_blueprint = Blueprint('graph', __name__)
graph_manager = GraphManager()

@graph_blueprint.route('/nodes', methods=['POST'])
def create_node():
    data = request.json
    node = graph_manager.create_node(data)
    if node:
        # After creating the node, update the graph view
        graph_manager.update_graph_view()
        # Return the updated graph data for the frontend to use
        graph_data = graph_manager.get_graph_data()
        return jsonify(graph_data), 201
    else:
        return jsonify({'error': 'Node creation failed'}), 400

@graph_blueprint.route('/nodes/<node_id>', methods=['GET'])
def get_node(node_id):
    node = graph_manager.find_node(node_id)
    if node is None:
        return jsonify({'message': 'Node not found'}), 404
    return jsonify(node.to_dict()), 200

# ... Other route definitions ...
