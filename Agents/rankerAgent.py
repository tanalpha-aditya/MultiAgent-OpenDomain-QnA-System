import json
from together import Together

def rerank_best_answer(json_files, config_file='config.json', model="meta-llama/Llama-3-8b-chat-hf"):
    # Load API key from configuration file
    with open(config_file, 'r') as file:
        config = json.load(file)

    together_ai_key = config.get("TOGETHER_AI")
    if not together_ai_key:
        raise ValueError("TOGETHER_AI key not found in the config file.")

    # Initialize Together client
    client = Together(api_key=together_ai_key)

    # Combine all JSON files into a single structure
    combined_prompts = {}
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Format the input for the prompt
        for item in data:
            query_id = item['query_id']
            if query_id not in combined_prompts:
                combined_prompts[query_id] = {
                    "question": item['input'],
                    "answers": {}
                }
            combined_prompts[query_id]["answers"][json_file] = item['response']

    responses = []

    for query_id, prompt in combined_prompts.items():
        # Generate the prompt text
        prompt_text = f"""Input JSON:
{json.dumps(prompt, indent=4)}

For the above question, identify which model gave the best response based on accuracy. Ensure the chosen response is an answer and not a follow-up question. Provide the output in the format:
{{
    "best_model": "<model_name>",
    "best_answer": "<answer>"
}}
Just output this JSON and nothing else.
"""

        # Generate response from Together API
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_text}],
        )
        response_content = response.choices[0].message.content 
        # print(response_content)

        prompt_text_extract_bestModel = f"""Input JSON:
{json.dumps(response_content, indent=4)}

Just Output the best_model from above JSON and nothing else.
"""
        prompt_text_extract_bestAnswer = f"""Input JSON:
{json.dumps(response_content, indent=4)}

Just Output the best_answer from above JSON and nothing else.
"""
        response_bestModel = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_text_extract_bestModel}],
        )
        response_bestAnswer = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt_text_extract_bestAnswer}],
        )
        
        # print({"query_id": query_id, "question": prompt["question"], "Ranker_Output": response.choices[0].message.content})
        responses.append({"query_id": query_id, "question": prompt["question"], "best_model": response_bestModel.choices[0].message.content, "best_answer": response_bestAnswer.choices[0].message.content})

        print(response_bestModel.choices[0].message.content)

    return responses


def rankerAgent(prompt, config_file='config.json', model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"):
    # Load API key from configuration file
    with open(config_file, 'r') as file:
        config = json.load(file)

    together_ai_key = config.get("TOGETHER_AI")
    if not together_ai_key:
        raise ValueError("TOGETHER_AI key not found in the config file.")

    # Initialize Together client
    client = Together(api_key=together_ai_key)

    prompt_text = f"""Input JSON:
{json.dumps(prompt, indent=4)}

For the above question, identify which model gave the best response based on accuracy. Ensure the chosen response is an answer and not a follow-up question. Provide the output in the format:
{{
    "best_model": "<model_name>",
    "best_answer": "<answer>"
}}
Just output this JSON and nothing else.
"""

    # Generate response from Together API
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text}],
    )
    response_content = response.choices[0].message.content 
    # print(response_content)

    prompt_text_extract_bestModel = f"""Input JSON:
{json.dumps(response_content, indent=4)}

Just Output the best_model from above JSON and nothing else.
"""
    prompt_text_extract_bestAnswer = f"""Input JSON:
{json.dumps(response_content, indent=4)}

Just Output the best_answer from above JSON and nothing else.
"""
    response_bestModel = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text_extract_bestModel}],
    )
    response_bestAnswer = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt_text_extract_bestAnswer}],
    )
        
    return response_bestModel.choices[0].message.content, response_bestAnswer.choices[0].message.content
    

# # Usage example
# json_files = ["../QnA_Eval/Responses/BOW_1_2_top_100_response.json",
#               "../QnA_Eval/Responses/BOW_1_2_top_100_modified_response.json",
#               "../QnA_Eval/Responses/tf-idf_1_2_top_100_response.json", 
#               "../QnA_Eval/Responses/tf-idf_1_2_top_100_modified_response.json",
#               "../QnA_Eval/Responses/bm25_1_2_top_100_response.json",
#               "../QnA_Eval/Responses/bm25_1_2_top_100_modified_response.json",
#               "../QnA_Eval/Responses/open_source_1_2_top_100_response.json", 
#               "../QnA_Eval/Responses/open_source_1_2_top_100_modified_response.json",
#               "../QnA_Eval/Responses/vision_1_2_top_100_response.json", 
#               "../QnA_Eval/Responses/vision_1_2_top_100_modified_response.json",
#               "../QnA_Eval/Responses/ZeroShot_response.json", 
#               "../QnA_Eval/Responses/WikiAgent_response.json",
#               "../QnA_Eval/Responses/WikiAgent_response_modified.json",
#               "../QnA_Eval/Responses/LlamaAgent_response.json",
#               "../QnA_Eval/Responses/LlamaAgent_response_modified.json",
#               "../QnA_Eval/Responses/tf_idf_bm25_open_1_2_top_100_combined_response.json", "../QnA_Eval/Responses/tf_idf_bm25_open_1_2_top_100_combined_modified_response.json", "../QnA_Eval/Responses/tf_idf_bm25_open_1_2_top_100_combined_both_response.json"]

# config_file = "../config.json"

# result = rerank_best_answer(json_files, config_file)

# with open("reranked_best_answers_1_2.json", 'w') as file:
#     json.dump(result, file, indent=4, ensure_ascii=False)
