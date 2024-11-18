import json
import os
from collections import defaultdict

def load_and_merge_json_files(directory_path):
    """
    Load and merge JSON files from a directory into a single structure, keeping each list from different files separate for each query.
    
    Args:
    directory_path (str): Path to the directory containing the JSON files.
    
    Returns:
    list: Merged list of dictionaries, keeping separate lists for each query.
    """
    merged_queries = defaultdict(list)
    
    # Iterate through all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            try:
                with open(file_path, 'r') as f:
                    json_data = json.load(f)
                    
                    # For each file, add the lists to the corresponding query
                    for query_data in json_data:
                        for query, rank_list in query_data.items():
                            if isinstance(rank_list, list):  # Ensure rank_list is a list
                                merged_queries[query].append(rank_list)
                            else:
                                print(f"Warning: Expected a list for query '{query}' but got {type(rank_list)}")
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    # Convert defaultdict to a list of dictionaries
    return [{query: lists} for query, lists in merged_queries.items()]

def reciprocal_rank_fusion(json_input, K=60, top_n=100):
    """
    Fuse rank from multiple IR systems for multiple queries using Reciprocal Rank Fusion.
    
    Args:
    json_input (list): A list of dictionaries where keys are queries, and values are ranked document lists from different systems.
    K (int): A constant used in the RRF formula (default is 60).
    top_n (int): Number of top results to return for each query.
    
    Returns:
    list: A list of dictionaries with each query and its respective fused document rankings.
    """
    query_fusion_results = []

    # Iterate over each query in the JSON input
    for query_data in json_input:
        for query, list_of_ranked_docs in query_data.items():
            rrf_map = defaultdict(float)

            # Fuse rankings for the query using RRF
            for rank_list in list_of_ranked_docs:
                for rank, doc in enumerate(rank_list, 1):
                    rrf_map[doc] += 1 / (rank + K)

            # Sort the documents based on RRF scores in descending order
            sorted_docs = sorted(rrf_map.items(), key=lambda x: x[1], reverse=True)
            fused_rankings = [doc for doc, score in sorted_docs[:top_n]]  # Keep only top N results

            # Store the results for the current query
            query_fusion_results.append({query: fused_rankings})

    return query_fusion_results

def save_to_json(output_data, output_file_path):
    """
    Save the RRF results to a JSON file in the same format as the input.
    
    Args:
    output_data (list): The processed data to save.
    output_file_path (str): Path to the output JSON file.
    """
    with open(output_file_path, 'w') as f:
        json.dump(output_data, f, indent=2)

# Example usage
directory_path = "Modified_1_2"  # Replace with your directory path
output_file_path = "Modified_1_2/rrf_1_2_modified.json"  # Replace with your desired output file path

# Load and merge JSON files
merged_input = load_and_merge_json_files(directory_path)

print(merged_input[0]["5xvggq"])

# Perform RRF on the merged input, keeping only the top 100 results
combined_results = reciprocal_rank_fusion(merged_input, top_n=100)

# Save the combined results to a JSON file
save_to_json(combined_results, output_file_path)

print(f"Combined results saved to {output_file_path}")


