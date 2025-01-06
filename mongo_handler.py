import pymongo
import requests

from huggingface_emeddings import get_embeddings

client = pymongo.MongoClient("mongodb+srv://jyothishkumarav:DjgQ5U6G8QzQc2Al@cluster0.qmpqq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client.sample_mflix
collection = db.movies

def embed_movies_plot():
    for doc in collection.find({'plot':{"$exists": True}}).limit(50):
      doc['plot_embedding_hf'] = get_embeddings(doc['plot'])
      collection.replace_one({'_id': doc['_id']}, doc)

def get_matching_result(query):
    results = collection.aggregate([
        {"$vectorSearch": {
            "queryVector": get_embeddings(query),
            "path": "plot_embedding_hf",
            "numCandidates": 100,
            "limit": 4,
            "index": "PlotSemanticSearch",
        }}
    ]);

    for document in results:
        print(f'Movie Name: {document["title"]},\nMovie Plot: {document["plot"]}\n')

def get_movie_with_pipeline(query):
    pipeline = [
        {
            '$vectorSearch': {
                'index': 'PlotSemanticSearch',
                'path': 'plot_embedding_hf',
                'queryVector': get_embeddings(query) ,
                'numCandidates': 150,
                'limit': 5
            }
        }, {
            '$project': {
                '_id': 0,
                'plot': 1,
                'title': 1,
                'score': {
                    '$meta': 'vectorSearchScore'
                }
            }
        }
    ]
    # run pipeline
    result = client["sample_mflix"]["movies"].aggregate(pipeline)
    for i in result:
        print(i)

if __name__ == "__main__":
    get_movie_with_pipeline('imaginary characters from outer space at war')