from flask_script import Manager
from app import app, db
from dbmodels import Case
import datetime
import json
import ast
import numpy as np
from models.embedding_model import extract_embeddings

manager = Manager(app)

with open('seed.json', 'r') as json_file:
  seed_data = json.load(json_file)


def format_date(date_str):
  if date_str:
    year = int(date_str.split('-')[0])
    month = int(date_str.split('-')[1])
    day = int(date_str.split('-')[2])
    return datetime.date(year, month, day)
  else:
    return None


@manager.command
def seed():
  print("Seeding the database...")

  try:
    mapped_seed_data = []

    for data in seed_data:
      data['open_date'] = format_date(data['open_date'])
      data['close_date'] = format_date(data['close_date'])
      data['embedding'] = np.array(extract_embeddings([data['case_text']])).tolist()[0]
      data['topic_verbs'] = ast.literal_eval(data['topic_verbs'])

      mapped_seed_data.append(Case(
        case_number = data['case_number'],
        case_text = data['case_text'],
        country = data['country'],
        open_date = data['open_date'],
        is_closed = data['is_closed'],
        close_date = data['close_date'],
        service = data['service'],
        embedding = data['embedding'],
        risk_score = data['risk_score'],
        topic_verbs = data['topic_verbs']
      ))

    db.session.add_all(mapped_seed_data)
    db.session.commit()

    print("Database seeded with {} cases!".format(len(mapped_seed_data)))

  except Exception as e:
    print(str(e))


if __name__ == "__main__":
  manager.run()
