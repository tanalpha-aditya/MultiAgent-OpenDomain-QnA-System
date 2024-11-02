import pandas as pd
import google.generativeai as genai

with open('api.key', 'r') as file:
    api_key = file.read().strip()

# Initialize the API key
genai.configure(api_key=api_key)

# Function to process text input with Gemini model
def modified_query(input_text):
    # Load the prompt from file
    with open("Query_Modification/prompt.txt", 'r') as file:
        prompt_maximum_weight_recommendation = file.read()

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

    
    full_prompt = f"{input_text}\n\n{prompt_maximum_weight_recommendation}"
                
    # Call the generative model for text input
    result = model.generate_content([full_prompt], safety_settings=safe)
    return result.text

