import tensorflow_hub as hub
model = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')

def extract_embeddings(query):
    return model(query)