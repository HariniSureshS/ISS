import tensorflow_hub as hub
import tensorflow_text
model = hub.load('https://tfhub.dev/google/universal-sentence-encoder-multilingual-large/3')

def extract_embeddings(query):
    return model(query)