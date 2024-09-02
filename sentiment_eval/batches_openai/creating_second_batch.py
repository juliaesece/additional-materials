import pandas as pd
import json

og_df = pd.read_csv("batches_openai/batch_all_climate_output.csv").set_index("custom_id")

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
                        {"role": "user", "content": row["message_content"]}
                    ],
                    "response_format": {
                        "type": "json_schema",
                        "json_schema": {
                              "name": "news_analysis",
                              "strict": True,
                              "schema": {
                                "type": "object",
                                "properties": {
                                  "is_about_climate_change": {
                                    "type": "boolean",
                                    "description": "If one of the main topics of the article is climate change"
                                  },
                                  "is_skeptical_about_climate_change": {
                                    "type": [
                                      "boolean",
                                      "null"
                                    ],
                                    "description": "If the article is dismissive or sceptical about climate change or its anthropocentric causes."
                                  },
                                  "cost_frame": {
                                    "type": [
                                      "boolean",
                                      "null"
                                    ],
                                    "description": "If the article discusses costs, losses and harms related to climate change."
                                  },
                                  "opportunity_frame": {
                                    "type": [
                                      "boolean",
                                      "null"
                                    ],
                                    "description": "If the article discusses opportunities, proactive solutions, and growth related to climate change. Solutions that are requiring restricting or reducing current activities don't count"
                                  },
                                  "overarching_sentiment": {
                                    "type": [
                                      "string",
                                      "null"
                                    ],
                                    "description": "Between the cost and opportunity frames, which one is given more attention? Choose between: cost, opportunity, or balanced."
                                  }
                                },
                                "required": [
                                  "is_about_climate_change",
                                  "is_skeptical_about_climate_change",
                                  "cost_frame",
                                  "opportunity_frame",
                                  "overarching_sentiment"
                                ],
                                "additionalProperties": False
                              }
                            }
                        }
                }
            }
            f.write(json.dumps(json_data) + '\n')
            
system_message = """
You are a json parser. You will receive text, summarise it, and convert it to the json schema that is specified.

If the solutions to climate change mentioned are about reducing something (like emissions), or restricting something, you will consider that the opportunity frame is false.
"""

i = 0
while i < len(og_df):
    df = og_df.iloc[i:(i+100)]
    convert_dataframe_to_json(df, system_message.replace('\n', ' '), 'batches_openai/to_json/climate_res_' + str(i) + '_to_' + str(i+100)+ '.jsonl')
    i = i + 100