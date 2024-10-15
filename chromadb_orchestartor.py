import chromadb
from uuid import uuid4



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
            metadatas=[{"tags": ", ".join(tags), "link": link}],
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
        # First, perform the search based on the query text to get the 10 nearest results
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        # If no search_tags, return the results as is
        if not search_tags:
            return results

        filtered_results = []  # List to store documents that match the search criteria

        # Iterate over the results
        for i, metadata in enumerate(results['metadatas']):
            # Get the tags from metadata and convert to a set
            doc_tags = set(tag.strip() for tag in metadata[i]['tags'].split(", "))  # Access tags correctly

            # Check if any of the search tags are in the document tags
            if any(tag in doc_tags for tag in search_tags):
                # If matched, extend the filtered_results with the corresponding document
                filtered_results.append(results['documents'][i])  # Append the document at index i

        # Return filtered results
        return filtered_results

#
#
# db_manager = ChromaDBManager("chroma_db_test1")
# # Add a feature
# # db_manager.add_feature("This sample Feature regarding the sand logic of slots", ["sand", "slot"], "http://link.com")
#
# # Search for features
# results = db_manager.search_features("slot logic", ['sand'])
# print(results)
# # Get all tags
# all_tags = db_manager.get_all_tags()
# # db_manager.update_tags_to_list_format()
# # results = db_manager.search_features('what is the slot logic in sand', ['sand'])
# #
# # # Display the search results
# # if results['documents']:
# #     features_combined = ""  # To store all the descriptions
# #
# #     for i, doc in enumerate(results['documents']):
# #         print(f"Feature {i + 1}: {doc}")
# #
# #         # Append feature description to the combined features list
# #         features_combined += f"\nFeature {i + 1}: {doc}"
# #     print(features_combined)