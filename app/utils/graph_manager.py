import json
import os
from app.services.node import Node

class GraphManager:
    def __init__(self, filename='nodes.json'):
        self.nodes = {}  # This will store nodes by their ID
        self.filename = filename
        self.load_nodes()  # Load nodes from file on initialization

    def save_nodes(self):
        with open(self.filename, 'w') as file:
            # Convert the nodes to a JSON-friendly format (e.g., list of dicts)
            # Include in_degree and out_degree in the node data
            nodes_data = [self.node_to_dict(node) for node in self.nodes.values()]
            json.dump(nodes_data, file)

    def load_nodes(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
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

    def calculate_degrees(self):
        in_degrees = {node_id: 0 for node_id in self.nodes}
        for node in self.nodes.values():
            for link in node.links:
                in_degrees[link.target_id] += 1
        return in_degrees

    def node_to_dict(self, node):
        in_degrees = self.calculate_degrees()
        node_dict = node.to_dict()
        node_dict['in_degree'] = in_degrees[node.id]
        node_dict['out_degree'] = len(node.links)
        return node_dict
