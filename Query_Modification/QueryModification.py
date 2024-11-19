import json
import pandas as pd
import google.generativeai as genai

# Function to process text input with Gemini model
def query_Modifier(input_text):

    with open('config.json', 'r') as file:
        config = json.load(file)

    gemini_key = config.get("GEMINI")

    # Initialize the API key
    genai.configure(api_key=gemini_key)

    # print(gemini_key)

    # Load the prompt from file
    with open("Query_Modification/prompt.txt", 'r') as file:
        PROMPT_TEMPLATE = file.read()

    # Safety settings for Gemini model
    safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Initialize the generative model
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

    
    full_prompt = f"{input_text}\n\n{PROMPT_TEMPLATE}"
                
    # Call the generative model for text input
    result = model.generate_content([full_prompt], safety_settings=safe)
    return result.text


def getKeywords(input_text):
    # Extract keywords from the input text

    with open('config.json', 'r') as file:
        config = json.load(file)

    gemini_key = config.get("GEMINI")

    # Initialize the API key
    genai.configure(api_key=gemini_key)

    # Safety settings for Gemini model
    safe = [
        {
            "category": "HARM_CATEGORY_DANGEROUS",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HARASSMENT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_NONE",
        },
    ]

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }
    
    # Initialize the generative model
    model = genai.GenerativeModel("gemini-1.5-flash", generation_config=generation_config)

    
    full_prompt = f"{input_text} \n\n Give the Keywords for the above sentence and output nothing else."
                
    # Call the generative model for text input
    result = model.generate_content([full_prompt], safety_settings=safe)

    response = result.text
    response = response.replace("Keywords:", "")
    response = response.replace(",", "")

    return response.strip()