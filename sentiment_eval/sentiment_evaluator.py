#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:56:49 2024

@author: juliasepulveda
"""

import numpy as np
import pandas as pd
import re
import random
from colorama import Back

class NewsSentimentAnalyzer:
    def __init__(self, csv_file, terms, force_new=False, random_seed=42):
        self.df = pd.read_csv(csv_file).set_index("article_id")
        self.force_new = force_new
        self.terms = terms
        self.pattern = '|'.join(f'({term})' for term in self.terms)
        
        random.seed(random_seed)
        np.random.seed(random_seed)
    
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

    def evaluate_news(self, start_at=0, sample_size=150):
        sample = self.df.sample(sample_size)
        sample["topic_evaluation"] = None
        sample["style_evaluation"] = None
        i = 0

        for index, row in sample.iterrows():
            if i < start_at:
                i += 1
                continue
            try:
                self.print_article(row)
                print("Evaluation #", i, "out of", sample_size)
                print(f"{Back.BLUE}TOPIC:{Back.RESET}")
                topic_evaluation = input("-1 for negative, 0 for neutral, 1 for positive: ")
                if not (topic_evaluation in ["-1", "0", "1"]):
                    topic_evaluation = input("-1 for negative, 0 for neutral, 1 for positive: ")
                print("You evaluated", topic_evaluation, "\n")
                sample.loc[index, "topic_evaluation"] = topic_evaluation
                print(f"{Back.RED}STYLE:{Back.RESET}")
                style_evaluation = input("-1 for negative, 0 for neutral, 1 for positive: ")
                if not (style_evaluation in ["-1", "0", "1"]):
                    style_evaluation = input("-1 for negative, 0 for neutral, 1 for positive: ")
                print("You evaluated", style_evaluation)
                sample.loc[index, "style_evaluation"] = style_evaluation
                i += 1
            except KeyboardInterrupt:
                print("Saving current and exiting")
                sample.to_csv('sentiment_eval_interrupted_at_' + str(i) + '_started_at_' + str(start_at) + '.csv')
                break

        return sample

def analyze_terms(csv_file, force_new=False):
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
    print("\nReading data...")
    analyzer = NewsSentimentAnalyzer(csv_file, terms)
    
    print("\nEvaluating news sample:")
    evaluated_sample = analyzer.evaluate_news()

    print("\nSaving evaluated news sample:")
    evaluated_sample.to_csv('df_sentiment_eval.csv')

def main():
    csv_file = "../climate_articles.csv"
    analyze_terms(csv_file)
    
    
if __name__ == "__main__":
    main()
