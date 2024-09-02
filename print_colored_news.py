#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 17 17:05:03 2024

@author: juliasepulveda
"""

from colorama import Back
import re

"""
Prints news text, highlighting words that are in the pattern (climate change words) for more readability
"""

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

pattern = '|'.join(f'({term})' for term in terms)

def color_text(text):
    return re.sub(pattern, Back.BLUE + r"\g<0>" + Back.RESET, text, flags=re.IGNORECASE)

def print_article(row):
    print(f"{Back.MAGENTA}Title:{Back.RESET} {color_text(row['title'])}\n")
    print(f"{Back.MAGENTA}ID:{Back.RESET} {row.name}\n")
    print(f"{Back.MAGENTA}content:{Back.RESET} {row['content']}\n")
    print(f"{Back.MAGENTA}full_content:{Back.RESET} {color_text(row['full_content'])}\n\n")
    print(f"{Back.MAGENTA}Title:{Back.RESET} {color_text(row['title'])}\n")
        
def print_colored_news(df):
    for _, row in df.iterrows():
        print_article(row)
        input("Press Enter to continue...")