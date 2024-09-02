#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:35:33 2024

@author: juliasepulveda
"""

import numpy as np
import pandas as pd
import re
import random

random.seed(42)
np.random.seed(42)

initial_pattern = r"(climat\w*\s*chang\w*)|(global\s*warm\w*)|(climate\s*crisis\w*)"

terms = [
    r'climat\w*\s*chang\w*', r'global\s*warm\w*', r'greenhouse\s*effect', r'greenhouse\s*gas\w*',
    r'emission\w*', r'climate\s*catastroph\w*', r'climate\s*disaster',
    r'carbon\s*emission\w*', r'climate\s*system', r'renewable\s*energ\w*', r'pollution',
    r'ipcc', r'carbon\s*dioxide', r'fossil\s*fuel\w*', r'carbon\s*footprint\w*',
    r'kyoto\s*protocol', r'paris\s*agreement', r'climate\s*conference\w*', r'climate\s*summit\w*',
    r'climate\s*poli\w*', r'climate\s*scien\w*', r'sea\s*level\s*ris\w*', r'climate\s*action\w*',
    r'two\s*degree\w*', r'sustainable',
    """MY ADDITION"""
    r'climate\s*protest\w*', r'climate\s*activis\w*',
    r'ocean\s*acidification', r'net[\s-]+zero', r'clean\s*energy', r'climate\s*crisis\w*',
    r'1\.5(\s|-)*(degree\w*|°?C|celsius)'
]

long_pattern = '|'.join(f'({term})' for term in terms)

print("Reading dataset...")
df = pd.read_csv("./clean_df.csv").set_index("article_id")

print("Creating initial selection...")
initial_search = df["full_content"].str.extract(initial_pattern, flags=re.IGNORECASE, expand=True)
positive_matches = initial_search.dropna(axis=0, how="all")
initial_selection = df.loc[positive_matches.index]

print("Creating final selection...")
count_matches = initial_selection['full_content'].str.count(long_pattern, flags=re.IGNORECASE)
three_or_more_matches = count_matches[count_matches.values >= 3] # Only keep articles with at least 3 keyword matches
final_selection = initial_selection.loc[three_or_more_matches.index]

print("Saving final selection to 'climate_articles.csv'")
final_selection.to_csv("climate_articles.csv")

print("\nNumber who mention climate change :", len(final_selection)) 
print("\nPercentage:", len(final_selection) * 100 / len(df))
