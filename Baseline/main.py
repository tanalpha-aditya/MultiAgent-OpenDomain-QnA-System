from data_processor import process_json_data, process_queries, merge_documents
from boolean_retrieval import main_boolean_retrieval
import json   


def main():
    # Load the JSON files
    with open("../Datasets/mini_wiki_collection.json", "r") as file1:  # Replace with the actual path to your file
        wikipedia_data = json.load(file1)

    with open("../Datasets/mini_wiki_collection_10000_documents.json", "r") as file1:  # Replace with the actual path to your file
        additional_json_file = json.load(file1)
    
    with open("../Datasets/FinalDataset_WithModifiedQuery.json", "r") as file2:  # Replace with the actual path to your file
        queries_data = json.load(file2)

    # Process the JSON files
    wikipedia_dict = process_json_data(wikipedia_data)
    updated_main_dict = merge_documents(wikipedia_dict, additional_json_file, limit=2000)
    queries_dict = process_queries(queries_data)

    # Print the processed data
    print("Processed Wikipedia Data:")
    print(wikipedia_dict["420538"])
    print("\nProcessed Queries Data:")
    print(queries_dict["5xvggq"])

    top_results = main_boolean_retrieval(updated_main_dict, queries_dict)

    # Print the results for a specific query
    print("\nTop results for query '5xvggq':")
    print(top_results.get("5xvggq", []))

    # Optionally, save the top results to a JSON file
    with open("boolean_retrieval_1_2_query.json", "w") as output_file:
        json.dump(top_results, output_file, indent=4)


if __name__ == "__main__":
    main()