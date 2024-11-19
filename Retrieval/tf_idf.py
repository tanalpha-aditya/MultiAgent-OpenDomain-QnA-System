import numpy as np
from collections import defaultdict
from gensim.utils import simple_preprocess
from tqdm import tqdm
import joblib


def get_tf_query(query):
    k = len(query)
    tf_query = defaultdict(lambda: 0)
    for i in range(k):
        tf_query[query[i]] += 1
    for token in tf_query.keys():
        tf_query[token] /= k
    return tf_query

def get_tf_idf_query(query, idf_dict):
    query = simple_preprocess(query)
    tf_idf_query = defaultdict(lambda: 0)
    tf_query = get_tf_query(query)
    for token in tf_query.keys():
        tf_idf_query[token] = tf_query[token] * idf_dict[token]
    return tf_idf_query
    
def get_tf_idf_vector(tf_idf_instance, vocab):
    temp = []
    for key in vocab.keys():
        temp.append(tf_idf_instance[key])
    return temp


def tf_idf_rankings(query, idf_dict, tf_idf_dict, vocab, document_matrix, k):
    query_vector = np.reshape(np.array(get_tf_idf_vector(get_tf_idf_query(query, idf_dict), vocab)), (1, -1))
    scores = []
    dot_products = document_matrix @ query_vector.T

    query_norm = np.linalg.norm(query_vector)
    doc_norms = np.linalg.norm(document_matrix, axis=1, keepdims=True)
    cosine_similarities = dot_products / (doc_norms * query_norm)
    cosine_similarities = cosine_similarities.flatten()
    rankings = np.argsort(cosine_similarities)[::-1]
    rankings = rankings[:k]
    scores = []
    for rank in rankings:
        scores.append(cosine_similarities[rank])
    # scores = sorted(cosine_similarities, key=lambda x: x[1], reverse=True)
    # scores = scores[:k]
    # rankings = get_documents_from_scores(scores)
    return rankings, scores

def tf_idf_pipeline(query, idf_dict_path="Retrieval/savedModels/idf.pkl", tf_idf_dict_path="Retrieval/savedModels/tf_idf_dict.pkl", vocab_path="Retrieval/savedModels/vocab.pkl", document_matrix_path="Retrieval/savedModels/document_matrix.pkl", ids_path="Retrieval/savedModels/ids.pkl", k=100):
    idf_dict = joblib.load(idf_dict_path)
    print("idf loaded...")
    tf_idf_dict = joblib.load(tf_idf_dict_path)
    print("tf-idf loaded...")
    vocab = joblib.load(vocab_path)
    print("vocab loaded...")
    document_matrix = joblib.load(document_matrix_path)
    print("document_matrix loaded...")
    ids = joblib.load(ids_path)
    print("ids loaded")
    rankings, scores = tf_idf_rankings(query, idf_dict, tf_idf_dict, vocab, document_matrix, k)
    rankings2 = []
    for ranking in tqdm(rankings):
        rankings2.append(ids[ranking])
    return rankings2