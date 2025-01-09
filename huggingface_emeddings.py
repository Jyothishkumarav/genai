import requests

# Define the API URL for the desired model
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
API_KEY = ""
HEADERS = {"Authorization": f"Bearer {API_KEY}"}

def get_embeddings(text):
    """
    Generate embeddings for input texts using a specific Hugging Face model.

    Args:
        text (str): List of sentences or paragraphs to generate embeddings for.

    Returns:
        list: A list of embeddings (one per input text).
    """
    # Format the input as required by the API
    payload = {"inputs": text}

    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API request failed with status code {response.status_code}: {response.text}")

# # Example usage
# input_text = "This is an example sentence."
# emb = get_embeddings(input_text)
# print(f"Embedding for input: {emb}...")
#