from collections import defaultdict
import re
import heapq
import joblib
import os

def preprocess_text(text):
    """
    Preprocess the text for tokenization.
    Removes special characters, lowercases, and splits into words.
    """
    return re.findall(r'\w+', text.lower())

def create_inverted_index(wikipedia_dict):
    """
    Create an inverted index from the document dictionary.
    Args:
        wikipedia_dict (dict): A dictionary with document IDs as keys and text as values.

    Returns:
        dict: An inverted index where each term maps to a list of document IDs containing it.
    """
    inverted_index = defaultdict(set)
    for doc_id, text in wikipedia_dict.items():
        tokens = set(preprocess_text(text))  # Unique tokens for each document
        for token in tokens:
            inverted_index[token].add(doc_id)
    return inverted_index

def save_inverted_index(inverted_index, filepath="Baseline/inverted_index.pkl"):
    """
    Save the inverted index to a file using joblib.
    """
    joblib.dump(inverted_index, filepath)

def load_inverted_index(filepath="Baseline/inverted_index.pkl"):
    """
    Load the inverted index from a file using joblib.
    """
    if os.path.exists(filepath):
        return joblib.load(filepath)
    return None

def boolean_retrieval(queries_dict, inverted_index, wikipedia_dict, top_n=100):
    """
    Perform boolean retrieval for each query.
    Args:
        queries_dict (dict): A dictionary with query IDs as keys and query text as values.
        inverted_index (dict): The inverted index created from the document collection.
        wikipedia_dict (dict): The original document dictionary (for scoring if needed).
        top_n (int): The number of top documents to retrieve for each query.

    Returns:
        dict: A dictionary with query IDs as keys and a list of top document IDs as values.
    """
    query_results = {}
    
    for query_id, query_text in queries_dict.items():
        query_tokens = preprocess_text(query_text)
        
        # Collect all document IDs that contain any of the query terms
        relevant_docs = set()
        for token in query_tokens:
            if token in inverted_index:
                relevant_docs.update(inverted_index[token])
        
        # If more than `top_n` documents, sort by some criteria (e.g., frequency of terms in the doc)
        doc_scores = []
        for doc_id in relevant_docs:
            doc_text = preprocess_text(wikipedia_dict[doc_id])
            score = sum(doc_text.count(token) for token in query_tokens)  # Term frequency score
            doc_scores.append((score, doc_id))
        
        # Get the top `top_n` documents based on the score
        top_docs = heapq.nlargest(top_n, doc_scores)
        query_results[query_id] = [doc_id for _, doc_id in top_docs]

    return query_results

# Main flow
def main_boolean_retrieval(wikipedia_dict, queries_dict):
    # Step 1: Create inverted index
    inverted_index = create_inverted_index(wikipedia_dict)
    
    # Step 2: Perform boolean retrieval
    top_docs = boolean_retrieval(queries_dict, inverted_index, wikipedia_dict)
    
    return top_docs

def retrieve_single_query(query, wikipedia_dict, top_n=100, inverted_index_path="Baseline/inverted_index.pkl"):
    """
    Retrieve documents for a single query using the inverted index.
    If the inverted index is not found, it will be created and saved.

    Args:
        query (str): The query text.
        wikipedia_dict (dict): The original document dictionary.
        top_n (int): The number of top documents to retrieve.
        inverted_index_path (str): Path to the saved inverted index file.

    Returns:
        list: A list of top document IDs matching the query.
    """
    # Load or create the inverted index
    inverted_index = load_inverted_index(inverted_index_path)
    if inverted_index is None:
        print("Inverted index not found. Creating one...")
        inverted_index = create_inverted_index(wikipedia_dict)
        save_inverted_index(inverted_index, inverted_index_path)

    # Preprocess the query
    query_tokens = preprocess_text(query)
    
    # Collect relevant documents
    relevant_docs = set()
    for token in query_tokens:
        if token in inverted_index:
            relevant_docs.update(inverted_index[token])
    
    # Rank documents by frequency of terms
    doc_scores = []
    for doc_id in relevant_docs:
        doc_text = preprocess_text(wikipedia_dict[doc_id])
        score = sum(doc_text.count(token) for token in query_tokens)
        doc_scores.append((score, doc_id))
    
    # Get the top `top_n` documents based on the score
    top_docs = heapq.nlargest(top_n, doc_scores)
    return [doc_id for _, doc_id in top_docs]

# Example usage:
# Assuming `wikipedia_dict` and `queries_dict` are already prepared
# top_results = main_boolean_retrieval(wikipedia_dict, queries_dict)
# print(top_results)
