from tqdm import tqdm
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer, util

# Load the model
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_documents_from_scores(scores):
    rankings = []
    for score in scores:
        rankings.append(score[0])
    return rankings

def cosine_similarity(v1, v2):
    v1 = np.array(v1)
    v2 = np.array(v2)
    if(np.linalg.norm(v1) != 0 and np.linalg.norm(v2) != 0):
        sim = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    else:
        sim = 0
    return sim

def get_open_source_embeddings(documents):
    documents_embeddings = []
    for document in tqdm(documents):
        documents_embeddings.append(model.encode(document))
    return documents_embeddings
    
def open_source_rankings(query, document_embeddings, k):
    query_embedding = model.encode(query)
    scores = []
    for idx, embedding in enumerate(document_embeddings):
        scores.append((idx, cosine_similarity(query_embedding, embedding)))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    scores = scores[:k]
    rankings = get_documents_from_scores(scores)
    return rankings, scores


def open_source_pipeline(query, documents_embeddings_path="Retrieval/savedModels/open_source_embeddings.pkl", ids_path="Retrieval/savedModels/ids.pkl", k=100):
    document_embeddings = joblib.load(documents_embeddings_path)
    ids = joblib.load(ids_path)
    rankings, scores = open_source_rankings(query, document_embeddings, k)
    rankings2 = []
    for ranking in tqdm(rankings):
        rankings2.append(ids[ranking])
    return rankings2