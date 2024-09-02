#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  5 15:42:10 2024

@author: juliasepulveda
"""

import pandas as pd
import re

terms = [
    r'climat\w*\s*chang\w*', r'global\s*warm\w*', r'climate\s*crisis\w*'
]

pattern = '|'.join(f'({term})' for term in terms)
weather_names = ["cyclone", "drought", "heatwave", "heavy_rain", "high_mountain", "wildfires"]

for event_name in weather_names:
    weather_df = pd.read_csv(event_name + "_final_selection.csv")
    
    print("\nNumber of articles on " + event_name + ":", len(weather_df))
    
    # Count how many matches
    count_all_keywords = weather_df['full_content'].str.count(pattern, flags=re.IGNORECASE)
    # Keep only the articles where there is at least one match
    meets_threshold = count_all_keywords[count_all_keywords > 0].index
    
    mentions_gw = weather_df.loc[meets_threshold]
    
    print("\nNumber who mention climate change :", len(mentions_gw)) 
    print("\nPercentage:", len(mentions_gw) * 100 / len(weather_df))

