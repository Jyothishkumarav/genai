from uuid import uuid4

import chromadb


class ChromaDBManager:
    def __init__(self, db_name):
        self.client = chromadb.PersistentClient(path=db_name)
        self.collection_name = "product_features"
        self.collection = self._create_or_get_collection()

    def _create_or_get_collection(self):
        if self.collection_name in [coll.name for coll in self.client.list_collections()]:
            return self.client.get_collection(self.collection_name)
        else:
            return self.client.create_collection(self.collection_name)

    def add_feature(self, feature_desc, tags, link):
        self.collection.add(
            documents=[feature_desc],
            metadatas=[{"tags": ", ".join(tags), "link": link, "status": "active"}],
            ids=[str(uuid4())]
        )

    def get_all_tags(self):
        results = self.collection.get(include=["metadatas"])
        all_tags = set()
        for metadata in results['metadatas']:
            tags = metadata.get("tags", "").split(", ")
            all_tags.update(tag.strip() for tag in tags if tag.strip())
        return list(all_tags)

    def search_features(self, query_text, search_tags=None, n_results=10):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        if not search_tags:
            return results

        filtered_results = []
        for i, metadata in enumerate(results['metadatas']):
            doc_tags = set(tag.strip() for tag in metadata[i]['tags'].split(", "))  # Access tags correctly

            # Check if any of the search tags are in the document tags
            if any(tag in doc_tags for tag in search_tags):
                # If matched, extend the filtered_results with the corresponding document
                filtered_results.append(results['documents'][i])  # Append the document at index i

            # Return filtered results
        return filtered_results

    def update_document_status(self, doc_id, new_status):
        # Fetch the document by its ID
        result = self.collection.get(ids=[doc_id])

        # Update the metadata status
        if result:
            metadata = result['metadatas'][0]
            metadata['status'] = new_status

            # Delete the old document and re-add it with updated metadata
            self.collection.delete(ids=[doc_id])
            self.collection.add(
                documents=result['documents'],
                metadatas=[metadata],
                ids=[doc_id]
            )
