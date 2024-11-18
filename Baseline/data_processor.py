# Assuming sanitize_text is a function you've defined elsewhere

import re

def merge_documents(main_dict, additional_json, limit=1000):
    """
    Adds a subset of documents from an additional JSON file to the main dictionary.

    Args:
        main_dict (dict): The main dictionary where processed documents are stored.
        additional_json (list): The additional JSON data containing documents.
        limit (int): The maximum number of documents to add to the main dictionary.

    Returns:
        dict: The updated main dictionary with additional documents added.
    """
    # Counter to track how many documents have been added
    count = 0

    for doc in additional_json:
        if count >= limit:
            break
        
        # Extract wikipedia_id and text from the document
        wikipedia_id = doc.get("wikipedia_id")
        text = doc.get("text", [])
        
        # Check if the document ID is unique to avoid overwriting
        if wikipedia_id not in main_dict:
            # Process and sanitize the document
            joined_text = " ".join(text)
            sanitized_text = sanitize_text(joined_text)
            
            # Add to the main dictionary
            main_dict[wikipedia_id] = sanitized_text
            count += 1
    
    print(f"{count} documents added to the main dictionary.")
    return main_dict

def sanitize_text(text):
    """
    Cleans and standardizes text by keeping only alphanumeric characters and spaces.
    Args:
        text (str): Text to sanitize.
    Returns:
        str: Sanitized text.
    """
    if isinstance(text, str):
        # Use regex to keep only alphanumeric characters and spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        # Optionally, collapse multiple spaces into a single space
        text = re.sub(r'\s+', ' ', text).strip()
    return text


def process_json_data(json_data):
    result_dict = {}
    
    for doc in json_data:
        # Extract wikipedia_id and text
        wikipedia_id = doc.get("wikipedia_id")
        text = doc.get("text", [])
        
        # Join the text content and sanitize
        joined_text = " ".join(text)
        sanitized_text = sanitize_text(joined_text)
        
        # Store in the dictionary
        result_dict[wikipedia_id] = sanitized_text

    return result_dict

def process_queries(json_data):
    """
    Processes a JSON object containing queries and query IDs.

    Args:
        json_data (dict): The input JSON data.

    Returns:
        dict: A dictionary with query_id as the key and query text as the value.
    """
    result_dict = {}
    
    for query_id, query_info in json_data.items():
        # Extract the query input
        query_text = query_info.get("input", "")
        
        # Store query_id and text in the result dictionary
        result_dict[query_id] = query_text

    return result_dict

# Example usage
# Assuming `query_json_file` contains your JSON data
# processed_queries = process_queries(query_json_file)

