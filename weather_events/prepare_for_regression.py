#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 16:58:07 2024

@author: juliasepulveda
"""

import pandas as pd
import re

terms = [
    r'climat\w*\s*chang\w*', r'global\s*warm\w*', r'climate\s*crisis\w*'
]

pattern = '|'.join(f'({term})' for term in terms)
weather_names = ["cyclone", "drought", "heatwave", "heavy_rain", "high_mountain", "wildfires"]
event_name = "high_mountain"
weather_df = pd.read_csv(event_name + "_countries_processed.csv")

df = pd.DataFrame(columns=weather_df.columns)
df["event"] = None
df["bias"] = None
df["country"] = None
df["adfontes_bias"] = None

official_countries = pd.read_csv("../sources/news_sources.csv", index_col=0)
countries = pd.read_csv("../sources/other_news_countries.csv", index_col=0)
sources =  pd.read_csv("../sources/all_sources_ratings_adfontes.csv")

for event_name in weather_names:
    weather_df = pd.read_csv(event_name + "_countries_processed.csv")
    weather_df["event"] = event_name
    print("\nNumber of articles on " + event_name + ":", len(weather_df))
    
    weather_df["bias"] = None
    weather_df["adfontes_bias"] = None
    weather_df["country"] = None
    for source in weather_df["source_name"].unique():
        if source in list(official_countries["name"]):
            weather_df.loc[weather_df["source_name"] == source, "country"] = official_countries.loc[official_countries["name"] == source, "country"].iloc[0]
        elif source in list(countries["source_name"]):
            weather_df.loc[weather_df["source_name"] == source, "country"] = countries.loc[countries["source_name"] == source, "source_country"].iloc[0]
        else:
            print(source, "not found")
            
    for index, row in sources.iterrows():
        weather_df.loc[weather_df["source_name"] == row["name"], "bias"] = row["bias"]
        weather_df.loc[weather_df["source_name"] == row["name"], "adfontes_bias"] = row["adfontes_bias"]

    cleaned_row = weather_df.loc[weather_df["source_name"] == "The Times of India", "full_content"].apply(lambda content: content.split("Experience Your Economic Times Newspaper")[0])
    weather_df.loc[weather_df["source_name"] == "The Times of India", "full_content"] = cleaned_row
    
    # Count how many matches
    count_all_keywords = weather_df['full_content'].str.count(pattern, flags=re.IGNORECASE)
    # Keep only the articles where there is at least one match
    meets_threshold = count_all_keywords[count_all_keywords > 0].index
    
    mentions_gw = weather_df.loc[meets_threshold]
    doesnt_mention =  weather_df.loc[~weather_df.index.isin(meets_threshold)]
    mentions_gw = mentions_gw.assign(mentions_gw=True)
    doesnt_mention = doesnt_mention.assign(mentions_gw=False)
    df = pd.concat([df, mentions_gw, doesnt_mention])
    
    
df = df.set_index("article_id")
df.columns
df.drop(inplace=True, axis=1, columns=['source_id', 'author', 'description', 'url',
        'url_to_image', 'published_at', 'content', 'category', 'full_content'])

df.to_csv("for_regressions_with_country.csv")