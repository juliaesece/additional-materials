import pandas as pd
import json

og_df = pd.read_csv("deduped_climate_articles.csv").set_index("article_id")

def convert_dataframe_to_json(df, system_message, output_file):
    with open(output_file, 'w') as f:
        for index, row in df.iterrows():
            json_data = {
                "custom_id": str(index),
                "method": "POST",
                "url": "/v1/chat/completions",
                "body": {
                    "temperature": 0.2,
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": system_message},
                        {"role": "user", "content": row["full_content"]}
                    ]
                }
            }
            f.write(json.dumps(json_data) + '\n')
            
system_message = """
You are a news analyser, paying attention to topics, styles, and frames. You will receive the content of a news article. Ignore data contamination. You will respond by answering the following questions:

1. What are the main topics of the article? Have that in mind when you answer the next questions.
2. Is climate change, its causes or consequences, one of those main topics? If it's not, stop your response.
For the following questions, focus on parts of the article that address climate change or things related to climate change.
1. Is this article dismissive or sceptical about climate change or its anthropocentric causes? If yes, stop your response.
2. Focus only on the main topics of the article. Are the costs, losses, restrictions, or harms related to or caused by climate change one of the main topics of the article? This includes whether or not it talks about restrictions needed to curb climate change. This is the "cost" frame.
3.a. Focus only on the main topics of the article. Are the opportunities, innovative solutions, or growth related to or caused by climate change one of the main topics of the article? This can be things like adaptation, resilience, innovation, green growth, or rewilding. 
3.b. Now, out of those solutions, discard the solutions that require reducing our current emissions, or restricting our activities. Are there any positive solutions left? This is the "opportunity"  frame. 
4. If both frames are present, estimate how many sentences are dedicated to each frame. Is one of the themes given significantly more importance than the other? If so, which one? If not, answer "balanced".
"""

i = 0
while i < len(og_df):
    df = og_df.iloc[i:(i+100)]
    convert_dataframe_to_json(df, system_message.replace('\n', ' '), 'all_climate_' + str(i) + '_to_' + str(i+100)+ '.jsonl')
    i = i + 100