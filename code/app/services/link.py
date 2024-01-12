links = []


class Link:
    def __init__(self, source_id, target_id):
        self.source_id = source_id
        self.target_id = target_id

    def to_dict(self):
        return {'source': self.source_id, 'target': self.target_id}

    def __repr__(self):
        return f"Link(source={self.source_id}, target={self.target_id})"
