from typing import List
from feature_service import FeatureService
from feature_dto import FeatureDTO

class FeatureController:
    def __init__(self):
        # Initialize the FeatureService with a ChromaDBManager instance
        from chromadb_manager import ChromaDBManager
        db_manager = ChromaDBManager("chroma_db_test1")
        self.feature_service = FeatureService(db_manager)

    def add_feature(self, feature_dto: FeatureDTO):
        """
        Handles the logic to add a new feature.
        """
        self.feature_service.add_feature(feature_dto)

    def update_feature_status(self, doc_id: str, new_status: str):
        """
        Handles updating the document status.
        """
        self.feature_service.update_feature_status(doc_id, new_status)

    def search_features(self, query_text: str, search_tags: List[str] = None,n_results=5):
        """
        Searches for features based on query and tags.
        """
        return self.feature_service.search_features(query_text, search_tags, n_results)

    def get_all_tags(self):
        """
        Retrieves all unique tags from the database.
        """
        return self.feature_service.get_all_tags()
