import json
import os
from app.services.node import Node
from app.services.link import Link

class GraphManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.nodes = {}
        self.filename = f'nodes_{self.user_id}.json'  # Unique filename for each user
        self.load_nodes()

    def save_nodes(self):
        with open(self.filename, 'w') as file:
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

    def add_link(self, source_id, target_id):
        source_id= int(source_id)
        target_id= int(target_id)
        if source_id not in self.nodes:
            raise ValueError(f"Node with id {source_id} does not exist.")
        if target_id not in self.nodes:
            raise ValueError(f"Node with id {target_id} does not exist.")
        source_node = self.nodes[source_id]
        target_node = self.nodes[target_id]

        # Check if the link already exists
        if any(link.target_id == target_id for link in source_node.links):
            raise ValueError(f"Link from node {source_id} to node {target_id} already exists.")

        # Add the link
        link = Link(source_id, target_id)
        source_node.links.append(link)
        self.save_nodes()

    def remove_link(self, source_id, target_id):
        if source_id not in self.nodes:
            raise ValueError(f"Node with id {source_id} does not exist.")
        if target_id not in self.nodes:
            raise ValueError(f"Node with id {target_id} does not exist.")
        source_node = self.nodes[source_id]

        # Find the index of the link to remove
        index_to_remove = None
        for i, link in enumerate(source_node.links):
            if link['target'] == target_id:
                index_to_remove = i
                break

        if index_to_remove is not None:
            del source_node.links[index_to_remove]
            self.save_nodes()
        else:
            raise ValueError(f"Link from node {source_id} to node {target_id} does not exist.")

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
