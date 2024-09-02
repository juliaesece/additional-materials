#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 15:45:52 2024

@author: juliasepulveda
"""

import numpy as np
import pandas as pd
import re
import random
from colorama import Back
import os


class NewsAnalyzer:
    def __init__(self, name, terms, force_new=False, random_seed=42, requiresTwoRounds=False, secondTerms=None):
        self.name = name
        self.terms = terms
        self.pattern = '|'.join(f'({term})' for term in self.terms)
        self.og_df = pd.read_csv("clean_df.csv").set_index("article_id")
        self.force_new = force_new
        self.lowest_f1_threshold = None
        if requiresTwoRounds:
            self.initPattern = '|'.join(f'({term})' for term in secondTerms)
            self.og_df = self.createInitialSelection(firstRound=True)
        self.createInitialSelection()
        
        random.seed(random_seed)
        np.random.seed(random_seed)
    
    def createInitialSelection(self, firstRound=False):
        """Selects all articles where at least one keyword in the list is found"""
        if os.path.isfile(self.name + "_initialSelection.csv") and not self.force_new:
            self.df = pd.read_csv(self.name + "_initialSelection.csv").set_index("article_id")
            print("\nSkipping making initial selection because already found...")
            print("\nLength of selection: ", len(self.df))
            return
        print("\nMaking initial selection...")
        if firstRound:
            searchResult = self.og_df["full_content"].str.extract(self.initPattern, flags=re.IGNORECASE, expand=True)
        else:
            searchResult = self.og_df["full_content"].str.extract(self.pattern, flags=re.IGNORECASE, expand=True)
        haveOneWord = searchResult.dropna(axis=0, how="all")
        initialSelection = self.og_df.loc[haveOneWord.index]
        self.df = initialSelection
        initialSelection.to_csv(self.name + '_initialSelection.csv')
        print("\nLength of selection:", len(initialSelection))
        return initialSelection

    def color_text(self, text):
        return re.sub(self.pattern, Back.BLUE + r"\g<0>" + Back.RESET, text, flags=re.IGNORECASE)

    def print_article(self, row):
        print(f"{Back.MAGENTA}Title:{Back.RESET} {self.color_text(row['title'])}\n")
        print(f"{Back.MAGENTA}ID:{Back.RESET} {row.name}\n")
        print(f"{Back.MAGENTA}content:{Back.RESET} {row['content']}\n")
        print(f"{Back.MAGENTA}full_content:{Back.RESET} {self.color_text(row['full_content'])}\n\n")
        print(f"{Back.MAGENTA}Title:{Back.RESET} {self.color_text(row['title'])}\n")

    def simple_print_news(self, sample_size=5):
        sample = self.df.sample(sample_size)
        for _, row in sample.iterrows():
            self.print_article(row)
            input("Press Enter to continue...")

    def evaluate_news(self, sample_size=50):
        sample = self.df.sample(sample_size)
        sample["Evaluation"] = None
        i = 1

        for index, row in sample.iterrows():
            self.print_article(row)
            print("Evaluation #", i, "out of", sample_size)
            evaluation = input("0 for No, 1 for Yes: ")
            print("You evaluated", evaluation)
            sample.loc[index, "Evaluation"] = evaluation
            input("Press Enter to continue...")
            i += 1

        return sample

    def analyze_keywords(self, df):
        print(df)
        count_keywords = df['full_content'].str.count(self.pattern, flags=re.IGNORECASE)
        
        try:
            totalPositives = df["Evaluation"].value_counts().loc[1]
        except KeyError:
            totalPositives = 0
        
        f1_scores = {}
        
        for threshold in range(0, 5):
            meets_threshold = count_keywords[count_keywords > threshold].index
            try:
                positives = df.loc[meets_threshold]["Evaluation"].value_counts().loc[1]
            except KeyError:
                positives = 0
            try:
                negatives = df.loc[meets_threshold]["Evaluation"].value_counts().loc[0]
            except KeyError:
                negatives = 0
            
            print(f"\nArticles with strictly more than {threshold} keyword mentions, aka at least {threshold+1} mentions:")
            print(f"Positives: {positives}, Negatives: {negatives}")
            if positives + negatives != 0:
                f1 = (2 * positives) / (2 * positives + negatives + (totalPositives - positives))
                f1_scores[threshold] = f1
                print(f"F1: {f1}")
            else:
                f1_scores[threshold] = 0  # Assign a high value when there are no positives or negatives
        
        self.lowest_f1_threshold = max(f1_scores, key=f1_scores.get)
        print(f"\nThreshold with the highest F1 value: {self.lowest_f1_threshold}")

        return count_keywords

    def filter_by_keyword_count(self):
        print(f"\nFiltering articles with  strictly more than {self.lowest_f1_threshold}:")
        count_all_keywords = self.df['full_content'].str.count(self.pattern, flags=re.IGNORECASE)
        meets_threshold = count_all_keywords[count_all_keywords > self.lowest_f1_threshold].index
        return self.df.loc[meets_threshold]


def analyze_terms(name, terms, force_new=False, skip_evaluation=False, requiresTwoRounds=False, secondTerms=None):
    print("\nReading data...")
    analyzer = NewsAnalyzer(name, terms, force_new=force_new, requiresTwoRounds=requiresTwoRounds, secondTerms=secondTerms)
    
    if (skip_evaluation):
        print("\nSkipping evaluating news sample:")
        evaluated_sample = pd.read_csv(name + '_evaluation.csv').set_index("article_id")
    else:
        print("\nEvaluating news sample:")
        evaluated_sample = analyzer.evaluate_news()
        print("\nSaving evaluated news sample:")
        evaluated_sample.to_csv(name + '_evaluation.csv')

    print("\nAnalyzing keywords in evaluated sample:")
    analyzer.analyze_keywords(evaluated_sample)


    filtered_df = analyzer.filter_by_keyword_count()
    print(f"Number of articles: {len(filtered_df)}")
    
    print("\nSaving results...")
    
    filtered_df.to_csv(name + '_final_selection.csv')

def main():
    # heatwave_terms = [
    #     r'Heat\s*wave\w*', r'Heatstroke\w*', r'Temperature\w* record\w*',
    #     r'Heat\w* record\w*', r'Heat\w* protection\w*', r'Heat\w* stress\w*',
    #     r'Heat-related death\w*', r'soaring temperature\w*', r'extreme heat',
    #     r'scorching',
    #     r'(hottest|warmest)( \w*)? (on record|recorded|in history|ever)', r"heat-related mortalit\w*"
    # ]
    # heatwave_name = "heatwave"
    # analyze_terms(heatwave_name, heatwave_terms, heatwave_csv)
    
    # heavy_rain_terms = [
    # r'Heavy\s*rain\w*', r'Heavy\s*precipitation\w*', r'Heavy\s*rainfall\w*',
    # r'Flood\s*disaster\w*', r'Inundation\w*', r'High\s*water\w*', r'River\s*level\w*',
    # r'Downpour\w*', r'Rain\s*intensity\w*',    r'Heavy\s*precipitation\s*amount\w*',
    # r'Precipitation\s*intensity\w*', r'Flash\s*flood\w*', r'Torrential\s*rain\w*',
    # r'Deluge\w*', r'Storm\s*surge\w*', r'flood\w*', r'Flood\s*warning\w*'
    # ]
    # heavy_rain_name = "heavy_rain"
    # analyze_terms(heavy_rain_name, heavy_rain_terms)
    #  looks like term is more than 1 (aka at least 2), but could be 3
    
    # init_wildfire_terms = [
    # r'wildfire\w*', r'fire\s*season\w*',
    # r'forest\w*\s*fire\w*', r'bushfire\w*',
    # ]
    
    # wildfire_terms = [
    # r'wildfire\w*', r'Inferno\w*',
    # r'Smoke\s*pollution\w*', r'Fire\s*containment\w*',r'fire\s*season\w*',
    # r'Scorched\s*earth\w*', r'forest\w*\s*fire\w*', r'bushfire\w*',
    # r'fire\s*crews\w*',  r'firefighter\w*', r'marsh\s*fire\w*'
    # ]
    
    # wildfire_name = "wildfires"
    # analyze_terms(wildfire_name, wildfire_terms, skip_evaluation=True)
    
    # drought_terms = [
    #     r'water\s*shortage\w*', r'arid\s*condition\w*', r'crop\s*failure\w*',
    #     r'dust\s*storm\w*', r'water\s*restriction\w*', r'desertification\w*',
    #     r'parched\s*land\w*', r'drought\w*'
    #     ]
    
    # drought_name = "drought"
    # analyze_terms(drought_name, drought_terms, skip_evaluation=True)
    
    # cyclone_terms = [
    #     r'cyclone\w*', r'hurricane\w*', 
    #     r'(?<!Al-Aqsa)(?<!desert)(?<!solar)(\W)storm(s?)(\W)',
    #     ]
    
    # cyclone_name = "cyclone"
    # analyze_terms(cyclone_name, cyclone_terms, skip_evaluation=True)
    
    high_mountain_terms = [
        r'landslide\w*',  r'avalanche\w*', r'rock\s*slide\w*',
        r'mud\s*slide\w*',r'debris\s*slide\w*',
        r'glacier\s*burst\w*',r'glacier\s*flood\w*',
        r'glacial\s*flood\w*',
    ]
    
    high_mountain_name = "high_mountain"
    analyze_terms(high_mountain_name, high_mountain_terms, skip_evaluation=True)
    
    
if __name__ == "__main__":
    main()