import pandas as pd
import google.generativeai as genai


# Initialize the API key
genai.configure(api_key="xxx")

# Function to process text input with Gemini model
def modified_query(input_text):
    # Load the prompt from file
    with open("prompt.txt", 'r') as file:
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

    # Initialize the generative model
    model = genai.GenerativeModel("gemini-1.5-flash")

    
    full_prompt = f"{input_text}\n\n{prompt_maximum_weight_recommendation}"
                
    # Call the generative model for text input
    result = model.generate_content([full_prompt], safety_settings=safe)
    return result.text

# # Run the function with text input instead of images
# input_text="Why can I fall asleep in noisy environments (school lectures, public transport, cinemas, etc) but an even lesser amount of noise can disturb my sleep when I'm in bed?"

# mod_query  = modified_query(input_text)
# print("Input Text :", input_text, "\n")
# print ("Modified Query: ", mod_query)