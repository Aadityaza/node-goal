class GraphView:
    def __init__(self, graph_manager):
        self.graph_manager = graph_manager

    def get_graph_data(self):
        # This function will convert the graph data into a format that can be
        # consumed by d3.js on the frontend.
        nodes = []
        links = []
        for node_id, node in self.graph_manager.nodes.items():
            nodes.append({'id': node.id, 'content': node.content})
            for link in node.links:
                links.append({
                    'source': link.source.id,
                    'target': link.target.id
                })
        return {'nodes': nodes, 'links': links}
