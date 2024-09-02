#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 26 15:54:24 2024

@author: juliasepulveda
"""

import pandas as pd
from remove_duplicate_text import remove_duplicates_in_df

def truncate_text(text, substring):
    parts = text.split(substring, 1)
    return parts[0] if len(parts) > 1 else text

raw_df = pd.read_csv("./global_news_dataset/data.csv")
df = raw_df.dropna(axis=0, subset=["full_content"])
df = df.drop_duplicates(subset="article_id", keep='first')
df = df.set_index("article_id")

print("The dataset has", len(raw_df), "rows")
print("After dropping dupplicats and NAs for full content, the dataset has", len(df), "rows")

print("Removing duplicated text in df, this might take a while...")
df = remove_duplicates_in_df(df)

print("Cleaning Phys articles.org")
phys = df[df["source_name"] == "Phys.Org"]

news_attributions = ['Provided byThe Conversation', '© 2023 AFPCitation', 'from https://phys.org']
for news_attribution in news_attributions:
    redundant_phys = phys[phys['full_content'].str.contains(news_attribution)]
    phys.loc[redundant_phys.index, 'full_content'] = redundant_phys['full_content'].apply(lambda x: truncate_text(x, news_attribution))

df.update(phys) # Modifies in place

print("Cleaning The Times of India articles")
times_of_india = df.loc[df["source_name"] == "The Times of India"]
cleaned_row = times_of_india["full_content"].apply(lambda content: content.split("Experience Your Economic Times Newspaper")[0])
df.loc[times_of_india.index, "full_content"] = cleaned_row

df.to_csv('clean_df.csv')  