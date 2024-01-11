class GraphView:
    def __init__(self, graph_manager):
        self.graph_manager = graph_manager

    def get_graph_data(self):
        nodes = []
        links = []
        for node_id, node in self.graph_manager.nodes.items():
            nodes.append({'id': node.id, 'content': node.content})
            for link in node.links:
                links.append(link.to_dict())  # Use the to_dict method of the Link class
        return {'nodes': nodes, 'links': links}

# class GraphView:
#     def __init__(self, graph_manager):
#         self.graph_manager = graph_manager
#
#     def get_graph_data(self):
#         # Dummy nodes data
#         nodes = [
#             {'id': 1, 'content': 'Node 1'},
#             {'id': 2, 'content': 'Node 2'},
#             {'id': 3, 'content': 'Node 3'}
#         ]
#
#         # Dummy links data
#         links = [
#             {'source': 1, 'target': 2},
#             {'source': 1, 'target': 3},
#             {'source': 2, 'target': 3}
#         ]
#
#         return {'nodes': nodes, 'links': links}
