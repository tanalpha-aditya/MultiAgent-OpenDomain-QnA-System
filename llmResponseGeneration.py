import json
import sys
import os
from AnswerGeneration.getAnswer import generate_answer_withContext

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def getRanking(file_path, query_id):
    ranking = load_json(file_path)
    # print(f"Ranking from file {file_path}: {ranking}")
    for rank in ranking:
        if query_id in rank:
            return str(rank[query_id][0])
    print("Query ID not found")
    return None

def getDocument(file_path1, file_path2, context_document_id):
    documents = load_json(file_path1)
    documents_irrelevant = load_json(file_path2)
    
    found = 0
    context_document_text = {}
    # Iterate over documents and check if any document matches the wikipedia_id
    for doc in documents:
        # Iterate through context_document_id to find the corresponding key (query_id)
        for query_id, wiki_id in context_document_id.items():
            # Check if the wikipedia_id matches the value (wiki_id)
            if wiki_id == doc["wikipedia_id"]:
                # Update the query_id with the joined text of the document
                context_document_text[query_id] = " ".join(doc["text"])  
                found += 1

    for doc in documents_irrelevant:
        # Iterate through context_document_id to find the corresponding key (query_id)
        for query_id, wiki_id in context_document_id.items():
            # Check if the wikipedia_id matches the value (wiki_id)
            if wiki_id == doc["wikipedia_id"]:
                # Update the query_id with the joined text of the document
                context_document_text[query_id] = " ".join(doc["text"])  
                found += 1

    print(f"Found {found} documents")
    return context_document_text

query_ids = load_json("QnA_Eval/QnA_Eval_Query_ids.json")
query = load_json("Datasets/FinalDataset_WithModifiedQuery.json")


# files = ["QnA_Eval/tf-idf_1_0_top_100.json", "QnA_Eval/tf-idf_1_1_top_100.json", "QnA_Eval/tf-idf_1_1_top_100_modified.json", "QnA_Eval/tf-idf_1_2_top_100.json", "QnA_Eval/tf-idf_1_2_top_100_modified.json", "QnA_Eval/open_source_1_0_top_100.json", "QnA_Eval/open_source_1_1_top_100.json", "QnA_Eval/open_source_1_1_top_100_modified.json", "QnA_Eval/open_source_1_2_top_100.json", "QnA_Eval/open_source_1_2_top_100_modified.json", "QnA_Eval/vision_1_1_top_100.json", "QnA_Eval/vision_1_1_top_100_modified.json"]

# files = ["QnA_Eval/vision_1_0_top_100.json", "QnA_Eval/vision_1_0_top_100_modified.json", "QnA_Eval/vision_1_2_top_100.json", "QnA_Eval/vision_1_2_top_100_modified.json", "QnA_Eval/tf-idf_1_0_top_100_modified.json", "QnA_Eval/open_source_1_0_top_100_modified.json"]

# files = ["QnA_Eval/BOW_1_0_top_100.json", "QnA_Eval/BOW_1_0_top_100_modified.json", "QnA_Eval/BOW_1_1_top_100.json", "QnA_Eval/BOW_1_1_top_100_modified.json", "QnA_Eval/BOW_1_2_top_100.json", "QnA_Eval/BOW_1_2_top_100_modified.json"]

# files = ["QnA_Eval/bm25_1_0_top_100.json", "QnA_Eval/bm25_1_0_top_100_modified.json", "QnA_Eval/bm25_1_1_top_100.json", "QnA_Eval/bm25_1_1_top_100_modified.json", "QnA_Eval/bm25_1_2_top_100.json", "QnA_Eval/bm25_1_2_top_100_modified.json"]

files = ["QnA_Eval/tf_idf_bm25_open_1_0_top_100_combined.json", "QnA_Eval/tf_idf_bm25_open_1_1_top_100_combined.json", "QnA_Eval/tf_idf_bm25_open_1_2_top_100_combined.json", "QnA_Eval/tf_idf_bm25_open_1_0_top_100_combined_modified.json", "QnA_Eval/tf_idf_bm25_open_1_1_top_100_combined_modified.json", "QnA_Eval/tf_idf_bm25_open_1_2_top_100_combined_modified.json", "QnA_Eval/tf_idf_bm25_open_1_0_top_100_combined_both.json", "QnA_Eval/tf_idf_bm25_open_1_1_top_100_combined_both.json", "QnA_Eval/tf_idf_bm25_open_1_2_top_100_combined_both.json"]


for file in files:
    results = []
    context_document_id = {}
    for query_id in query_ids:
        context_document_id[query_id] = getRanking(file, query_id)

    miniWikiCollection_path_irrelevant = "Datasets/mini_wiki_collection_10000_documents.json"
    miniWikiCollection_path = "Datasets/mini_wiki_collection.json"
    context_documents = getDocument(miniWikiCollection_path, miniWikiCollection_path_irrelevant, context_document_id)

    print(f"Number of queries: {len(query_ids)}")
    for query_id in query_ids:
        context_text = context_documents[query_id]
        context_text = context_text[:1500]
        query_text = query[query_id]["input"]
        if file.endswith("modified.json"):
            query_text = query[query_id]["modified_query"]
        answer_text = list(query[query_id]["output"].values())[0]
        response = generate_answer_withContext(query_text, context_text)
        results.append({
            "query_id": query_id,
            "top_document_id": context_document_id[query_id],  
            "input" : query_text,
            "response": response,
            "gold_answer": answer_text
        })
        # print(results)
        # break

    with open(f"QnA_Eval/Responses/{file.split("/")[-1][:-5]}_response.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)