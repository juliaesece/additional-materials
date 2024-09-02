#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 18 19:47:56 2024

@author: juliasepulveda
"""

from collections import Counter
import en_core_web_sm
import pandas as pd
from geopy.geocoders import Nominatim
import re
import pickle

nlp = en_core_web_sm.load()

flat_countries = None

with open("flat_countries", "rb") as fp:   # Unpickling flat countries object
    flat_countries = pickle.load(fp)

# Lowercase and remove everything that isn't letters for better matches 
# For US, U.S. -> us 
def strip_country(text):
    text = text.lower()
    pattern = r'[^a-z]'
    text = re.sub(pattern, '', text)
    return text

def read_country(location):
    """
    Find country based on location
    """
    try:
        location = geolocator.geocode(location, language="en")
    except Exception as e:
        print (e) # Sometimes there is a retry error
        return "error"
    if not location:
        print("Not found")
        return "not found"
    country = location.address.split(',')[-1] # Split the string based on comma and retruns the last element (country)
    return strip_country(country)

print("Loading df...")
geolocator = Nominatim(user_agent="news_climate_project")

weather_names = ["heavy_rain", "high_mountain", "wildfires", "cyclone", "drought", "heatwave",]

for event_name in weather_names:
    df = pd.read_csv(event_name + "_final_selection.csv").set_index("article_id")
    
    print("Will search", len(df), "rows")
    df["countries_mentioned"] = None
    total = len(df)
    i = 0
    
    for index, row in df.iterrows():
        text = row["full_content"]
    
        print("Processing row", index, "and", total - i, "left")
        doc = nlp(text)
        
        locations = [X.text for X in doc.ents if X.label_ == "GPE"]
        locations = Counter(locations)
        print("Found entities", locations)
        print()
        # Convert all GPE entities to their respective countries and store in a list
        mentioned_countries = []
        
        # Iterating through the counter ensures we only search each location once
        for location in locations:
            print("Searching", location)
            # First search in the countries list
            if strip_country(location) in flat_countries:
                # Append country, the amount of times it was counted as that's important information
                mentioned_countries.extend([strip_country(location)] * locations[location])
            # If not found, search with geopy
            else: 
                mentioned_countries.extend([read_country(location)] * locations[location])
                
        final_locations = Counter(mentioned_countries)
        print(final_locations)
        print()
        final_locations_list = list(final_locations.elements()) # Make into a list as Counters aren't supported
        df.at[index, "countries_mentioned"] = final_locations_list # Store in dataframe
        i = i + 1

    df.to_csv(event_name + "_with_countries.csv")
