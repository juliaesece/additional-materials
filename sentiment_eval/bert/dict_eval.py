#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 20 04:49:44 2024

@author: juliasepulveda
"""

import numpy as np
from polarities import sentiment_dict
import pandas as pd
from sklearn.metrics import classification_report
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# sentiment_eval_0_to_100
eval_df = pd.read_csv("../sentiment_eval_0_to_100.csv").set_index("article_id") # style_evaluation, topic_evaluation
eval_df["bert_eval"] = None

sentiment_df = pd.DataFrame.from_dict(sentiment_dict, orient="index", columns=["polarity"])
sentiment_df = sentiment_df.sort_values(by=['polarity'])
mean = np.mean(sentiment_df["polarity"])
std = np.std(sentiment_df["polarity"])
low_cut = mean - (std * 3)
high_cut = mean + (std * 3)

lemmatizer = WordNetLemmatizer()

pos_words = sentiment_df.loc[sentiment_df["polarity"] > high_cut]
neg_words = sentiment_df.loc[sentiment_df["polarity"] < low_cut]

pos_words = [lemmatizer.lemmatize(token) for token in pos_words.index]
neg_words = [lemmatizer.lemmatize(token) for token in neg_words.index]


def get_sentiment(text):
    text = row["full_content"]
    tokens = word_tokenize(text.lower())
    filtered_tokens = [token for token in tokens if token not in stopwords.words('english')]

    lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
    
    pos = 0
    neg = 0
    for lemma in lemmatized_tokens:
        if lemma in pos_words:
            pos = pos + 1
        elif lemma in neg_words:
            neg = neg + 1

    max_val = max(pos, neg)
    if max_val == 0:
        return 0
    diff = pos - neg
    if (abs(diff) * 100 / max_val) < 30:
        return 0
    elif diff > 0:
        return 1
    else:
        return -1

for idx, row in eval_df.iterrows():
    sentiment = get_sentiment(row["full_content"])
    eval_df.at[idx, "dict_eval"] = sentiment
    
results_eval = classification_report(eval_df["topic_evaluation"], eval_df["dict_eval"])
eval_df["dict_eval"].value_counts()
print(results_eval)
