class GraphManager:
    def __init__(self):
        self.nodes = {}  # This will store nodes by their ID for quick access

    def add_node(self, node):
        # Assuming node has a unique 'id' attribute
        if node.id in self.nodes:
            raise ValueError(f"Node with id {node.id} already exists.")
        self.nodes[node.id] = node

    def update_node(self, node_id, new_content):
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist.")
        self.nodes[node_id].content = new_content  # Simple content update logic

    def delete_node(self, node_id):
        if node_id not in self.nodes:
            raise ValueError(f"Node with id {node_id} does not exist.")
        del self.nodes[node_id]

    def find_node(self, node_id):
        return self.nodes.get(node_id, None)

    # Additional methods to manage links could be here...
