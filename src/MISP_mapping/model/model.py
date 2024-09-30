from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.cluster import KMeans
from MISP_mapping.model.data import get_example_texts_with_topics
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")


def encode_text(text):
    """Encode text to embeddings using pre-trained transformer model."""
    inputs = tokenizer(
        text, return_tensors="pt", padding=True, truncation=True, max_length=512
    )
    outputs = model(**inputs)
    return outputs.pooler_output.detach().numpy().flatten()


def get_example_texts():
    return [x[0] for x in get_example_texts_with_topics()]


texts = get_example_texts()
embeddings = np.array([encode_text(text) for text in texts])

kmeans = KMeans(n_clusters=2, random_state=42).fit(embeddings)


def cluster_to_topic(cluster_label):
    topic_names = {}
    for i, e in enumerate([x[1] for x in get_example_texts_with_topics()]):
        topic_names[i] = e
    return topic_names.get(cluster_label, "Unknown")


def get_topic_for_row(row_text):
    row_embedding = encode_text(row_text).reshape(1, -1)

    cluster_label = kmeans.predict(row_embedding)[0]
    return cluster_to_topic(cluster_label)
