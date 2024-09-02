#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 19 16:30:35 2024

@author: juliasepulveda
"""

import pandas as pd
import numpy as np
from sklearn.metrics import classification_report

result_df = pd.read_csv('batches_openai/to_json/batch_res_climate_output.csv')

eval_df = pd.read_csv("sentiment_eval_0_to_100.csv").set_index("article_id")

# Checking internal consistency
print("Checking internal consistency")
only_cost = result_df.loc[result_df["cost_frame"] == True]
only_cost = only_cost.loc[only_cost["opportunity_frame"] != True]
print(only_cost["overarching_sentiment"].value_counts(normalize=True))

only_opportunity = result_df.loc[result_df["opportunity_frame"] == True]
only_opportunity = only_opportunity.loc[only_opportunity["cost_frame"] != True]
print(only_opportunity["overarching_sentiment"].value_counts(normalize=True))

pred_df = result_df.loc[eval_df.index]
# Mapping words to numbers
pred_df["nb_eval"] = np.where(
    pred_df["overarching_sentiment"] == "balanced", 0, np.where(
    pred_df["overarching_sentiment"] == "opportunity", 1, -1)) 

print("Evaluation of the model:")
results_eval = classification_report(eval_df["topic_evaluation"], pred_df["nb_eval"])
print(results_eval)