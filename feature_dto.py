from typing import List

class FeatureDTO:
    def __init__(self, description: str, tags: List[str], link: str, status: str = "active"):
        self.description = description
        self.tags = tags
        self.link = link
        self.status = status
