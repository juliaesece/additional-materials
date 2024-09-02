# Extended research project
**Title**: Evaluating Climate Communication in News Media Using Computational Methods

**Description**: The report aims to answer the following research questions:

**RQ1**: With which frequency are unusual or extreme weather events explicitly linked to cli-
mate change, and how does this vary depending on the event, the location of the event,
and the country and political orientation of the newspaper?

**RQ2**: With which frequency is reporting on climate change news positive, neutral or neg-
ative, and how does this vary depending on the country and the political orientation of the
newspaper?

The objective of this repository is to allow for the reproduction of the methods used in said report, not to provide a ready-made package or an easily reusable code base.

## 1. Table of Contents
- [Installation](#2.-installation)
- [Data](#data)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Methods](#methods)

## 2. Installation
### Python
This project was developed using Python and Anaconda, which you need to have installed in your machine. Due to conflicting packages, three different environments where necessary: LDA, tokenization, and socialsent.
To recreate the environments, you can run

```
conda env create -f env_[env_name].yml
conda activate [env_name]
```

However, there are some known issues with the portability of the yml file between different OS systems. If you encounter these issues, you can manually install the dependencies listed in the `env_[env_name]_deps_only.yml` for each environment. 

I have provided the polarities generated in the project, however, if you want to recreate the SocialSent polarities, you have to download the project from this [link](https://github.com/williamleif/socialsent), and use the socialsent environment. 

### R
The regressions in this project where ran using R 4.4.1 in Posit Cloud. You will need the libraries `MASS` (it was run using version 7.3.61) and `marginaleffects` (it was run using version 0.21.0).

## 3. Data
- **Data Source**: To start, download data.csv from this [link](https://www.kaggle.com/datasets/everydaycodings/global-news-dataset/data?select=data.csv) and place it in the "global_news_dataset" folder.
- **Data Description**: The global news dataset contains articles from news sources around the world. We are mainly interested in the news sources, title and full (text) content.
- **Preprocessing Steps**:  Run `clean_df.py` to clean the data and produce `clean_df.csv`.

## 4. Usage

### Run the code for RQ1
#### (Optional) Reprocess the dataset
1. Go to the `weather_events` folder
2. If you want to create your own evaluation benchmark, you can run `OOP eval keywords.py`. This will create a `initial_selection`, `evaluation` and `final_selection` csv files for each weather event.
3. Run `calculate_mention_frequency.py` to calculate mention frequencies per weather event.
4. If you have modified the dataset and want to get the locations mentioned, run `location_tagger.py` and then `mentions_country.py`. This will create `with_countries` and `countries_processed` csv files, respectively. Note: these scripts take a long time to run (about 1h).
5. Run `prepare_for_regression.py`, which will create the datasets that will then be used in R, and copy it to the `regressions_in_R` folder

#### Run the regressions
1. Go to the `regressions_in_R` folder
2. Run `log_regressions.R`

### Run the code for RQ2
#### (Optional) Reprocess the dataset and recreate the evaluation benchmark
1. Run `create_climate_df.py` to create the climate dataset for RQ2
2. Run `sentiment_evaluator.py` to create the evaluation benchmark
#### Dictionary method
1. Go to the `sentiment_eval/bert` folder
2. Run `dict_eval.py` for the simple dictionary method, and `bert_single.py` for the version that is augmented with BERT embeddings.
#### LLM method
##### (Optional) Reprocess the dataset
1. Go to the `sentiment_eval/batches_openai` folder
2. Run `creating_first_bactch.py` to create the batch for the first stage of prompting. Due to OpenAI's rate limitations, this outputs files with the format `number_to_number`, which can then be submited one by onte. Submit the outputed .jsonl files on the OpenAI paltform, as Batches (more information on Batches documentation can be found [here](https://platform.openai.com/docs/guides/batch/overview)). Download the results as `batch_climate_res_*_to_*_output.jsonl`. 
3. Run `batches_json_to_df.py`, which will create `batch_all_climate_output.csv`
4. Run `creating_second_batch.py`, which will instruct the model to parse the previous responses as JSON. Save the results as `batch_climate_res_*_to_*_output.jsonl` in the `to_json` folder.
5. Run `to_json/batches_msg_json_to_df`. This will create `batch_res_climate_output.csv`.
6. Run `for_regressions_sentiment.py` to create the dataset which will be used to run the ordered regression in R.

##### Evaluate the results
1. Run `results_openai.py`. This will print the classification report for the LLM method.
2. Go to the `regressions_in_R` folder
3. Run `ordered_logit.R`.

## 5. **Project Structure**
```
├── global_news_dataset
│   └── data.csv             # Place raw data here
│
├── weather_events                               # Files for RQ1 (weather events)
│   ├── evaluate_keywords.py                     # Script to evaluate keywords
│   ├── calculate_mention_frequency.py           # Script to calculate climate change mention frequency
│   ├── location_tagger.py                       # Script to add all mentioned countries in an article
│   ├── mentions_country.py                      # Script to add a "mentions_own_country" boolean feature
│   ├── prepare_for_regression.py                # Script to generate the .csv file used for the regresssions in R
│   ├── [event_name]_final_selection.csv         # Dataset containing the selected articles for each weather event
│   ├── [event_name]_countries_processed.csv     # Dataset containing the selected articles for each weather event, plus             
│   │                                            # "mentions_own_country"
│   ├── for_regressions_with_country.csv         # Dataset used for regressions in R
│   └── print_colored_news.py                    # Util used by other scripts
│
├── sentiment_eval                               # Files for RQ2 (sentiment/frame eval)
│   ├── batches_openai                           # Scripts to create and process batches for OpenAi
│   │   ├── creating_first_batch.py              # Script to create batch from .csv files, creates
│   │   │                                        # 'all_climate_' + str(i) + '_to_' + str(i+100)+ '.jsonl' files
|   |   ├── batches_json_to_df.py                # Creates batch_all_climate_output.csv 
│   │   ├── creating_second_batch.py             # Takes batch_all_climate_output.csv and creates .jsonl files for second stage 
│   │   └── to_json
│   │      └── batches_msg_json_to_df.py        # Takes batch_climate_res_*_to_*_output.jsonl files and generates the final output
│   │
│   ├── bert
│   |   ├── dict_eval.py               # Sentiment evaluation dataset
│   |   ├── bert_single.py             # Script for processing OpenAI results
│   |   └── polarities.py              # Polarities generated with SentEval
│   │
│   ├── results_openai.py              # Script to generate evaluation metrics for the LLM method
│   ├── sentiment_evaluator.py         # Script to generate the evaluation benchmark
│   └──sentiment_eval_0_to_100.csv     # Evaluation benchmark
│   
├── sources                               # Data on news sources
│   ├── all_sources_ratings_adfontes.csv  # MBFC and AdFontes media bias ratings
│   ├── news_sources.csv                  # CSV containing news sources information (from NewsAPI)
│   └── other_news_countries.csv          # CSV containing news sources information for the sources that were missing in NewsAPI
│
├── regressions_in_R                              # Data and R scripts
│   ├── for_regressions_with_country.csv          # CSV file for regression analysis
│   ├── log_regressions.R                         # R script for regression logging
│   └── R regressions ERP.Rproj                   # R project file
│
├── clean_df.py                   # Script to preprocess raw data (data.csv)
├── create_climate_df.py          # Script to create climate_articles.csv
├── print_colored_news.py         # Util used by other scripts
├── remove_duplicate_text.py      # Util used by other scripts
├── env_[env_name].yml            # Files with the dependencies used
└── README.md                     # Project documentation
```