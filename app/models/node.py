class Node:
    def __init__(self, id, content, links, metadata):
        self.id = id
        self.content = content
        self.links = links
        self.metadata = metadata

    def to_dict(self):
        # Convert the node instance into a dictionary for JSON serialization
        return {
            'id': self.id,
            'content': self.content,
            'links': [link.to_dict() for link in self.links],
            'metadata': self.metadata.to_dict()
        }
