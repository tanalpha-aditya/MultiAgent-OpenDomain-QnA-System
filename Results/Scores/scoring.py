import os
import json
import pandas as pd

def calculate_scores(directory, output_excel):
    # Initialize a list to store results
    results = []

    # Iterate through all files in the directory
    for file_name in os.listdir(directory):
        if file_name.endswith('.json'):  # Process only JSON files
            file_path = os.path.join(directory, file_name)
            with open(file_path, 'r') as file:
                try:
                    data = json.load(file)
                    score = 0
                    # Calculate score as the sum of reciprocal of rank
                    for item in data:
                        rank = item.get("rank", 0)
                        if rank > 0:  # Avoid division by zero
                            score += 1 / rank
                    results.append({"File Name": file_name, "Score": score})
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in file: {file_name}")
    
    # Convert results to a DataFrame
    df = pd.DataFrame(results)
    
    # Save the DataFrame to an Excel file
    df.to_excel(output_excel, index=False)
    print(f"Scores have been saved to {output_excel}")

# Example usage
directory = "all_file"
output_excel = "ranking_scores.xlsx"
calculate_scores(directory, output_excel)
