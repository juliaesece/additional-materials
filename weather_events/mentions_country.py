#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 02:15:43 2024

@author: juliasepulveda
"""
import pandas as pd
import numpy as np
from collections import Counter
import ast
from countries_list import countries, strip_country

country_lookup = {}

for country_set in countries:
    country_lookup[country_set[0].lower()] = strip_country(country_set[1])

country_lookup["eu"] = "europe"
country_lookup["af"] = "africa"


np.set_printoptions(suppress=True) # Disable scientific notation

weather_names = ["cyclone", "drought", "heatwave", "heavy_rain", "high_mountain", "wildfires"]

for event_name in weather_names:
    population_csv = event_name + "_with_countries.csv"
    population_name = event_name
    
    print("Reading " + event_name + " df...")
    population_df = pd.read_csv(population_csv).set_index("article_id")
    print("It has", len(population_df), "rows")
    
    population_df["country"] = None
    population_df["mentions_own_country"] = False
    population_df["about_own_country"] = False
    
    official_countries = pd.read_csv("../sources/news_sources.csv", index_col=0)
    countries = pd.read_csv("../sources/other_news_countries.csv", index_col=0)
    
    # Store source information in df
    for source in population_df["source_name"].unique():
        if source in list(official_countries["name"]):
            population_df.loc[population_df["source_name"] == source, "country"] = official_countries.loc[official_countries["name"] == source, "country"].iloc[0]
        elif source in list(countries["source_name"]):
            population_df.loc[population_df["source_name"] == source, "country"] = countries.loc[countries["source_name"] == source, "source_country"].iloc[0]
        else:
            print(source, "not found")
    
    for idx, row in population_df.iterrows():
        country = country_lookup[row["country"]]
        countries_mentioned_list = ast.literal_eval(row["countries_mentioned"]) # Parse list string back into python list
        if len(countries_mentioned_list) == 0:
            continue
        mentioned_counter = Counter(countries_mentioned_list)
        if country in countries_mentioned_list or row["country"] in countries_mentioned_list:
            population_df.at[idx, "mentions_own_country"] = True
        if country == mentioned_counter.most_common(1)[0][0]:
            population_df.at[idx, "about_own_country"] = True
    
    population_df.to_csv(population_name + '_countries_processed.csv')