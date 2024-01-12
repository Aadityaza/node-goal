from app.services.parser import *


class Metadata:
    def __init__(self, creation_date, last_modified_date, tags):
        self.creation_date = creation_date
        self.last_modified_date = last_modified_date
        self.tags = tags  # List of strings


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
        self.links = Parser.parse(self.content, self.id)

    def to_dict(self):
        # Convert the node instance into a dictionary for JSON serialization
        return {
            'id': self.id,
            'content': self.content,
            'links': [link.to_dict() for link in self.links],
            'metadata': self.metadata.to_dict()
        }
