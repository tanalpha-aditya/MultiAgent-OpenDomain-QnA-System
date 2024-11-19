import json
from together import Together

def generate_article_from_query(query, config_file='config.json', model="meta-llama/Llama-3-8b-chat-hf"):
    """
    Generates an article based on the given query using the Together API.

    Parameters:
    - query (str): The input query for generating the article.
    - config_file (str): Path to the JSON file containing the API key. Default is 'config.json'.
    - model (str): The Together AI model to use. Default is "meta-llama/Llama-3-8b-chat-hf".

    Returns:
    - str: The generated article content.
    """
    # Load API key from configuration file
    with open(config_file, 'r') as file:
        config = json.load(file)

    together_ai_key = config.get("TOGETHER_AI")
    if not together_ai_key:
        raise ValueError("TOGETHER_AI key not found in the config file.")

    # Initialize Together client
    client = Together(api_key=together_ai_key)

    # Create the prompt
    prompt = f"""Using the query provided, generate a well-researched and informative short article. The article should be detailed, accurate, and structured to cover various aspects of the topic in an engaging way. Focus on presenting key facts, historical context, notable insights, and any relevant background information that adds value to the reader’s understanding. Ensure the tone is neutral and informative. Keep the article short. Here’s the query:

    Query: {query}"""

    # Generate response
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

# # Example usage
# if __name__ == "__main__":
#     query = "I feel anxious about my health and stressed at work."
#     article = generate_article_from_query(query)
#     print(article)
