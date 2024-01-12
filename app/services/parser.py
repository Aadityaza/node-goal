import re
from app.services.link import *


class Parser:
    @staticmethod
    def parse(content, node_id):
        links = []
        pattern = r"\[\[(.*?)\]\]"
        matches = re.findall(pattern, content)

        for match in matches:
            try:
                # Convert target to integer
                target_id = int(match)
                link = Link(node_id, target_id)
                links.append(link)
            except ValueError:
                # Handle the case where the target is not an integer
                # For example, log an error, skip, or handle differently
                print(f"Invalid link target '{match}' in node {node_id}")

        return links
