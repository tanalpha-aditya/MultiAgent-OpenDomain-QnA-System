import numpy as np
import joblib
from gensim.utils import simple_preprocess
from rank_bm25 import BM25Okapi

def bm25_pipeline(query, bm25_path="Retrieval/savedModels/bm25-1_0.pkl", ids_path="Retrieval/savedModels/ids.pkl", k=100):
    bm25 = joblib.load(bm25_path)
    ids = joblib.load(ids_path)
    ranking = bm25.get_scores(simple_preprocess(query))
    ranking = np.argsort(np.array(ranking))[::-1]
    ranking = ranking[:k]
    for j in range(len(ranking)):
        ranking[j] = ids[ranking[j]]
    return ranking