import json
from app.services.node import Node
import os
class GraphManager:
    def __init__(self, filename='nodes.json'):
        self.nodes = {}  # This will store nodes by their ID
        self.filename = filename
        self.load_nodes()  # Load nodes from file on initialization

    def save_nodes(self):
        with open(self.filename, 'w') as file:
            # Convert the nodes to a JSON-friendly format (e.g., list of dicts)
            json.dump([node.to_dict() for node in self.nodes.values()], file)

    def load_nodes(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            # If the file does not exist or is empty, start with an empty set of nodes
            self.nodes = {}
            return

        with open(self.filename, 'r') as file:
            nodes_list = json.load(file)
            for node_data in nodes_list:
                node = Node.from_dict(node_data)
                self.nodes[node.id] = node

    def add_node(self, node):
        if node.id in self.nodes:
            raise ValueError(f"Node with id {node.id} already exists.")
        self.nodes[node.id] = node
        self.save_nodes()

    def update_node(self, node_id, new_content):
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist.")
        self.nodes[node_id].content = new_content
        self.save_nodes()

    def delete_node(self, node_id):
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist.")
        del self.nodes[node_id]
        self.save_nodes()

    def find_node(self, node_id):
        return self.nodes.get(node_id, None)