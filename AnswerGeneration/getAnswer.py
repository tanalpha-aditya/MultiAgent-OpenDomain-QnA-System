import os
import json
from together import Together

def generate_answer_withContext(question, context):
    with open('config.json', 'r') as file:
        config = json.load(file)

    together_ai_key = config.get("TOGETHER_AI")

    client = Together(api_key=together_ai_key) 

    prompt = f"""Consider the context and generate a brief 1-2 line answer to the question. Output only the answer.

Context: {context}

Question: {question}
"""
    response = client.chat.completions.create(
        # model="meta-llama/Llama-3-8b-chat-hf",
        model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content


def generate_answer_zeroShot(question):
    with open('config.json', 'r') as file:
        config = json.load(file)

    together_ai_key = config.get("TOGETHER_AI")

    client = Together(api_key=together_ai_key)

    prompt = f"""Answer the following question:

Question: {question}
"""
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-8b-chat-hf",
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content
