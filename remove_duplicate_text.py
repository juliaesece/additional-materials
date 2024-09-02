#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 16:09:20 2024

@author: juliasepulveda
"""

import re
from collections import defaultdict

def remove_duplicates_in_df(df):
    print("Removing duplicates text from df full_content...")
    def remove_duplicates(text):
        # Normalize the text
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Split the text into sentences
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        # Create a hash of sentence groups
        sentence_hash = defaultdict(list)
        for i, sentence in enumerate(sentences):
            sentence_hash[sentence].append(i)
        
    
        # Find duplicate groups
        duplicate_groups = [indices for sentence, indices in sentence_hash.items() if len(indices) > 1]
        if len(duplicate_groups) == 0:
            return text

        # Sort duplicate groups by their first occurrence
        duplicate_groups.sort(key=lambda x: x[0])
        
        # Remove duplicates
        to_remove = set()
        for group in duplicate_groups:
            # Keep the first occurrence, mark others for removal
            to_remove.update(group[1:])
        
        # Reconstruct the text without duplicates
        clean_sentences = [sent for i, sent in enumerate(sentences) if i not in to_remove]
        clean_text = ' '.join(clean_sentences)
        
        return clean_text
    
    # Example usage
    for index, row in df.iterrows():
        clean_text = remove_duplicates(row["full_content"])
        df.loc[index, "full_content"] = clean_text
    
    return df
