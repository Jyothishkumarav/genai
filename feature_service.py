from uuid import uuid4
from typing import List
from feature_dto import FeatureDTO

class FeatureService:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_feature(self, feature_dto: FeatureDTO):
        """
        Adds a new feature to the database.
        """
        doc_id = str(uuid4())
        metadata = {
            "tags": ", ".join(feature_dto.tags),
            "link": feature_dto.link,
            "status": feature_dto.status
        }
        # Add the document with the provided metadata and ID
        self.db_manager.add_document(feature_dto.description, metadata, doc_id)

    def update_feature_status(self, doc_id: str, new_status: str):
        """
        Updates the status of an existing feature.
        """
        document = self.db_manager.get_document(doc_id)
        if document:
            metadata = document['metadatas'][0]
            metadata['status'] = new_status
            self.db_manager.update_document(doc_id, metadata)

    def search_features(self, query_text: str, search_tags: List[str] = None, n_results: int = 5):
        """
        Searches for features in the database, filtering by query and tags.
        """
        results = self.db_manager.query_documents(query_text, n_results)
        if search_tags:
            filtered_results = []
            for i, metadata in enumerate(results['metadatas']):
                doc_tags = set(tag.strip() for tag in metadata[i]['tags'].split(", "))
                if any(tag in doc_tags for tag in search_tags):
                    filtered_results.append(results['documents'][i])
            return filtered_results
        return results['documents']

    def get_all_tags(self):
        """
        Retrieves all unique tags from the metadata in the database.
        """
        all_metadata = self.db_manager.get_all_metadata()
        all_tags = set()
        for metadata in all_metadata['metadatas']:
            tags = metadata.get("tags", "").split(", ")
            all_tags.update(tags)
        return list(all_tags)
