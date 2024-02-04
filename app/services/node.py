from app.services.parser import *
from datetime import datetime


class Metadata:
    def __init__(self, creation_date, last_modified_date):
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date

    def to_dict(self):
        return {
            'creation_date': self.creation_date.isoformat() if self.creation_date else None,
            'last_modified_date': self.last_modified_date.isoformat() if self.last_modified_date else None,
        }


def calculate_metadata():
    # You can calculate the creation_date and last_modified_date here
    # For example:
    from datetime import datetime
    creation_date = datetime.now()
    last_modified_date = datetime.now()

    # Create a Metadata object with the calculated values
    metadata = Metadata(creation_date, last_modified_date)

    return metadata


class Node:
    def __init__(self, id, content,type):
        self.id = id
        self.content = content
        self.metadata = calculate_metadata()
        #self.links = Parser.parse(self.content, self.id)  # Outgoing links
        self.links= []
        self.type = type # goal or task

    def size(self, in_degree=0):
        # Calculate size based on content length and in-degree
        return len(self.content) + in_degree * 10  # Adjust the formula as needed

    def to_dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'links': [link.to_dict() for link in self.links],
            'metadata': self.metadata.to_dict(),
            'type': self.type,
            'size': self.size()  # Call size method without in_degree here

        }

    @classmethod
    def from_dict(cls, data):
        id = data['id']
        content = data['content']
        type = data['type']

        node = cls(id, content,type)
        node.links = [Link.from_dict(link_data) for link_data in data['links']]

        # Handle creation and last modified date
        node.metadata.creation_date = datetime.fromisoformat(data['metadata']['creation_date'])
        node.metadata.last_modified_date = datetime.fromisoformat(data['metadata']['last_modified_date'])

        return node

