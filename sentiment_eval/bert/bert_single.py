#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 17:35:12 2024

@author: juliasepulveda
"""

import torch
from transformers import BertTokenizer, BertModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from polarities import pos_seeds, neg_seeds, sentiment_dict
import pandas as pd
from pprint import pp
from sklearn.metrics import classification_report

eval_df = pd.read_csv("../sentiment_eval_0_to_100.csv").set_index("article_id")
eval_df["bert_eval"] = None

sentiment_df = pd.DataFrame.from_dict(sentiment_dict, orient="index", columns=["polarity"])
sentiment_df = sentiment_df.sort_values(by=['polarity'])
mean = np.mean(sentiment_df["polarity"])
std = np.std(sentiment_df["polarity"])
low_cut = mean - (std * 1)
high_cut = mean + (std * 1)

pos_words = sentiment_df.loc[sentiment_df["polarity"] > high_cut]
neg_words = sentiment_df.loc[sentiment_df["polarity"] < low_cut]

# Initialize BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Set the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

# Create a dictionary of sentiment words with their polarities
sentiment_words = { 
    'pos_general': ["good", "successful", "beneficial", "help"],
    "pos_hope": ["hope"],
    "pos_progress": ["improve", "advancement"],
    'pos_environment': ["renewable", "sustainable", "green", "clean", "durable", "ecofriendly"],
    'pos_conservation': ["conservation", "save", "protection", "restoration"],
    "pos_technology": ["innovation", "efficient", "optimal", "enhancement", "effective", "useful"],
    "pos_solution": ["solution", "fix"],
    "bal_reduction": ["reduce", "decrease", "lower"],
    "neg_environment": ["emissions", "pollution"],
    "neg_general": ["wrong", "bad", "worst"],
    "neg_fail": ["fail"],
    "neg_cost": ["cost", "costly", "expensive"],
    "neg_loss": ["erode", "lose", "loss", "extinction"],
    "neg_damage": ["damage", "destruction", "kill", "harm", "hurt", "suffer", "hazard"],
    "neg_catastrophe": ["disaster", "catastrophe", "famine", "tragic", "danger"]
}

def get_bert_embedding(word):
    """Get BERT embedding for a single word."""
    inputs = tokenizer(word, return_tensors='pt', padding=True, truncation=True, max_length=12).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    return outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()

# Create sentiment embedding dictionary
sentiment_embeddings = {}
for sentiment, words in sentiment_words.items():
    sentiment_embeddings[sentiment] = np.mean([get_bert_embedding(word) for word in words], axis=0)

def analyze_sentiment(text):
    """Analyze sentiment of given text using BERT embeddings and sentiment dictionary."""
    # Tokenize and get BERT embeddings for the input text
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=128).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    text_embedding = outputs.last_hidden_state.mean(dim=1).squeeze().cpu().numpy()
    
    results = {}
    for sentiment_key in sentiment_embeddings.keys():
        # Calculate cosine similarity with positive and negative sentiment embeddings
        results[sentiment_key] = cosine_similarity(text_embedding.reshape(1, -1), 
                                                sentiment_embeddings[sentiment_key].reshape(1, -1))[0][0]

    return results


for idx, row in eval_df.iterrows():
    sentiment = analyze_sentiment(row["content"])
    print(f"Text: {row['title']}")
    # print(f"Text: {row['description']}")
    sorted_sentiment = sorted(sentiment.items(), key=lambda x:x[1], reverse=True)
    sorted_sentiment = sorted_sentiment[0:5]
    print("Sentiment:")
    pp(sorted_sentiment)
    eval_sent = 0
    eval_diff = sentiment['pos_environment'] - sentiment['neg_environment']
    if abs(eval_diff) < 0.01:
        eval_sent = 0
    elif eval_diff > 0:
        eval_sent = 1
    else:
        eval_sent = -1
    print(f"Diff: {eval_diff:.4f}")
    print(f"eval_sent: {eval_sent}")
    eval_df.at[idx, "bert_eval"] = eval_sent
    print()

eval_df["topic_evaluation"].value_counts()
eval_df["bert_eval"].value_counts()

eval_df["bert_eval"] = eval_df["bert_eval"].values.astype('float64')
results_eval = classification_report(eval_df["topic_evaluation"], eval_df["bert_eval"])
print(results_eval)
