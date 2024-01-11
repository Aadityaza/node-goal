import re
from app.services.link import *

class Parser:
    @staticmethod
    def parse(content, node_id):
        links = []
        pattern = r"\[\[(.*?)\]\]"
        matches = re.findall(pattern, content)

        for match in matches:
            link = Link(node_id, match)
            links.append(link)

        return links