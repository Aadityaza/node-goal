from app.services.parser import *
from datetime import datetime


class Metadata:
    def __init__(self, creation_date, last_modified_date, tags):
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date
        self.tags = tags  # List of strings

    def to_dict(self):
        return {
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'last_modified_date': self.last_modified_date.isoformat() if self.last_modified_date else None,
            'tags': self.tags
        }


def calculate_metadata(tags):
    # You can calculate the creation_date and last_modified_date here
    # For example:
    from datetime import datetime
    creation_date = datetime.now()
    last_modified_date = datetime.now()

    # Create a Metadata object with the calculated values
    metadata = Metadata(creation_date, last_modified_date, tags)

    return metadata


class Node:
    def __init__(self, id, content, tags):
        self.id = id
        self.content = content
        self.metadata = calculate_metadata(tags)
        self.links = Parser.parse(self.content, self.id)  # Outgoing links
        self.size = len(content)
        self.in_degree = 0  # Initially zero, to be updated based on incoming links
        self.out_degree = len(self.links)  # Calculated from outgoing links

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'links': [link.to_dict() for link in self.links],
            'metadata': self.metadata.to_dict(),
            'size': self.size,
            'in_degree': self.in_degree,
            'out_degree': self.out_degree
        }

    # Method to update in-degree, typically called when another node links to this node
    def update_in_degree(self, increment=True):
        if increment:
            self.in_degree += 1
        else:
            self.in_degree -= 1

    # Method to update out-degree, typically called when this node links to or removes a link to another node
    def update_out_degree(self, increment=True):
        if increment:
            self.out_degree += 1
        else:
            self.out_degree -= 1

    @classmethod
    def from_dict(cls, data):
        id = data['id']
        content = data['content']
        tags = data['metadata']['tags']

        node = cls(id, content, tags)

        # Assuming you store links as a list of dictionaries in 'links' key
        # and you have a Link class with a similar from_dict method.
        node.links = [Link.from_dict(link_data) for link_data in data['links']]

        node.size = data['size']
        node.in_degree = data['in_degree']
        node.out_degree = data['out_degree']

        # Handle creation and last modified date
        node.metadata.creation_date = datetime.fromisoformat(data['metadata']['creation_date'])
        node.metadata.last_modified_date = datetime.fromisoformat(data['metadata']['last_modified_date'])

        return node
