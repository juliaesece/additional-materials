#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 23:18:30 2024

@author: juliasepulveda
"""
import json
import pandas as pd
import logging
import glob
import re

# Set up logging
logging.basicConfig(filename='processing_errors.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

def process_jsonl_file(file_path):
    data = []
    
    with open(file_path, 'r') as file:
        for line in file:
            try:
                # Parse the JSON line
                json_data = json.loads(line)
                
                # Check the status code
                if json_data['response']['status_code'] != 200:
                    logging.error(f"Error in response for custom_id {json_data['custom_id']} in file {file_path}: "
                                  f"Status code {json_data['response']['status_code']}")
                    continue
                
                # Extract the required information
                custom_id = json_data['custom_id']
                message_content = json_data['response']['body']['choices'][0]['message']['content']
                message_dict = json.loads(message_content)
                
                # Append to the data list
                new_line = {'custom_id': custom_id}
                new_line.update(message_dict)
                data.append(new_line)

            except KeyError as e:
                logging.error(f"KeyError in JSON structure in file {file_path}: {e}")
            except json.JSONDecodeError:
                logging.error(f"Invalid JSON in line in file {file_path}: {line}")
            except Exception as e:
                logging.error(f"Unexpected error processing line in file {file_path}: {e}")
    
    return data

def process_all_files(file_pattern):
    all_data = []
    
    # Get all files matching the pattern
    files = glob.glob(file_pattern)
    
    # Sort files based on the numeric range in their names
    files.sort(key=lambda x: int(re.search(r'(\d+)_to_(\d+)', x).group(1)))
    
    for file_path in files:
        print(f"Processing file: {file_path}")
        file_data = process_jsonl_file(file_path)
        all_data.extend(file_data)
    
    # Create the DataFrame from all collected data
    df = pd.DataFrame(all_data)
    return df

file_pattern = 'batch_climate_res_*_to_*_output.jsonl'
result_df = process_all_files(file_pattern)

not_about_climate_change = result_df.loc[result_df["is_about_climate_change"] == False]
skeptical = result_df.loc[result_df["is_skeptical_about_climate_change"] == True]
skeptical_ids = [int(_) for _ in skeptical["custom_id"]]

# Display the total number of rows in the DataFrame
print(f"Total rows in DataFrame: {len(result_df)}") # Should be 1127

# Save the DataFrame to a CSV file
result_df.to_csv('batch_res_climate_output.csv', index=False)
