import datetime
import json
import ast
import numpy as np
import pandas as pd
from models.embedding_model import extract_embeddings
from settings import *


with open(DATA_ROOT, 'r') as json_file:
  seed_data = json.load(json_file)


def format_date(date_str):
  if date_str:
    year = int(date_str.split('-')[0])
    month = int(date_str.split('-')[1])
    day = int(date_str.split('-')[2])
    return datetime.date(year, month, day)
  else:
    return None

def load_data():
  print("Loading")

  try:

    for data in seed_data:
      data['open_date'] = format_date(data['open_date'])
      data['close_date'] = format_date(data['close_date'])
      data['embedding'] = np.array(extract_embeddings([data['case_text']])).tolist()[0]
      data['topic_verbs'] = ast.literal_eval(data['topic_verbs'])

    df =pd.DataFrame.from_records(seed_data)
    print("Loading{} cases!".format(len(seed_data)))
    return df

  except Exception as e:
    print(str(e))

  