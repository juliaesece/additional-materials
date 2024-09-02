#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 16:10:46 2024

@author: juliasepulveda
"""

import pandas as pd
 
result = pd.read_csv("batch_res_climate_output.csv").set_index("custom_id")
df = pd.read_csv("../../../climate_articles.csv").set_index("article_id")

merged_df = df.join(result)

merged_df["bias"] = None
merged_df["country"] = None
merged_df["adfontes_bias"] = None

official_countries = pd.read_csv("../../../sources/news_sources.csv", index_col=0)
countries = pd.read_csv("../../../sources/other_news_countries.csv", index_col=0)
sources =  pd.read_csv("../../../sources/all_sources_ratings_adfontes.csv")

for source in merged_df["source_name"].unique():
    if source in list(official_countries["name"]):
        merged_df.loc[merged_df["source_name"] == source, "country"] = official_countries.loc[official_countries["name"] == source, "country"].iloc[0]
    elif source in list(countries["source_name"]):
        merged_df.loc[merged_df["source_name"] == source, "country"] = countries.loc[countries["source_name"] == source, "source_country"].iloc[0]
    else:
        print(source, "not found")

for source in merged_df["source_name"].unique():
    if source in list(official_countries["name"]):
        merged_df.loc[merged_df["source_name"] == source, "country"] = official_countries.loc[official_countries["name"] == source, "country"].iloc[0]
    elif source in list(countries["source_name"]):
        merged_df.loc[merged_df["source_name"] == source, "country"] = countries.loc[countries["source_name"] == source, "source_country"].iloc[0]
    else:
        print(source, "not found")

for index, row in sources.iterrows():
    merged_df.loc[merged_df["source_name"] == row["name"], "bias"] = row["bias"]
    merged_df.loc[merged_df["source_name"] == row["name"], "adfontes_bias"] = row["adfontes_bias"]

merged_df.drop(inplace=True, axis=1, columns=['source_id', 'author', 'description', 'url',
        'url_to_image', 'published_at', 'content', 'category', 'full_content', 'event'])

merged_df.to_csv("for_regressions_sentiment.csv")
