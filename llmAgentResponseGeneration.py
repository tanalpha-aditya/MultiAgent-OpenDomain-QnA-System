from Query_Modification.QueryModification import modified_query, getKeywords
from Agents.togetherAIAgent import generate_article_from_query
from Agents.wikiAgent import get_wiki_data
# from AnswerGeneration.getAnswer import generate_answer
from Ranking.RRF.RRF_implementation import reciprocal_rank_fusion
from AnswerGeneration.getAnswer import generate_answer_withContext, generate_answer_zeroShot
import json

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    

query_ids = load_json("QnA_Eval/QnA_Eval_Query_ids.json")
query = load_json("Datasets/FinalDataset_WithModifiedQuery.json")

results = []
ct = 0

for query_id in query_ids:
    query_text = query[query_id]["modified_query"]
    answer_text = list(query[query_id]["output"].values())[0]
    response = generate_answer_zeroShot(query_text)
    results.append({
        "query_id": query_id,
        "context": "",  
        "input" : query_text,
        "response": response,
        "gold_answer": answer_text
    })


with open(f"QnA_Eval/Responses/ZeroShot_response_modified.json", "w") as f:
    json.dump(results, f, indent=4, ensure_ascii=False)

# for query_id in query_ids:
#     query_text = query[query_id]["input"]
#     # context_text = generate_article_from_query(query_text)
#     keywords = getKeywords(query_text)
#     wiki_data = get_wiki_data(keywords)
#     if(wiki_data is None):
#         answer_text = list(query[query_id]["output"].values())[0]
#         response = generate_answer_zeroShot(query_text)
#         results.append({
#             "query_id": query_id,
#             "context": "",  
#             "input" : query_text,
#             "response": response,
#             "gold_answer": answer_text
#         })
#         continue
#     context_text = wiki_data[0]
#     context_text = context_text[:1500]
#     answer_text = list(query[query_id]["output"].values())[0]
#     response = generate_answer_withContext(query_text, context_text)
#     results.append({
#         "query_id": query_id,
#         "context": context_text,  
#         "input" : query_text,
#         "response": response,
#         "gold_answer": answer_text
#     })
#     ct += 1
#     print(ct)
#     # print(results)
#     # break

# with open(f"QnA_Eval/Responses/WikiAgent_response.json", "w") as f:
#     json.dump(results, f, indent=4, ensure_ascii=False)