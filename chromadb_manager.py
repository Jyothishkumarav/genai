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

    def add_document(self, description, metadata, doc_id):
        """
        Adds a document to the collection.
        """
        self.collection.add(
            documents=[description],
            metadatas=[metadata],
            ids=[doc_id]
        )

    def get_document(self, doc_id):
        """
        Retrieves a document by ID.
        """
        return self.collection.get(ids=[doc_id])

    def update_document(self, doc_id, metadata):
        """
        Updates the metadata of a document by deleting the old document and adding it again.
        """
        result = self.get_document(doc_id)
        if result:
            self.collection.delete(ids=[doc_id])
            self.collection.add(
                documents=result['documents'],
                metadatas=[metadata],
                ids=[doc_id]
            )

    def query_documents(self, query_text, n_results=10):
        """
        Queries the documents based on text.
        """
        return self.collection.query(query_texts=[query_text], n_results=n_results)

    def get_all_metadata(self):
        """
        Retrieves all metadata from the collection.
        """
        return self.collection.get(include=["metadatas"])
