from flask_script import Manager
from app import app, db
from dbmodels import Case
import json
import ast
import numpy as np
from models.embedding_model import extract_embeddings
import re

manager = Manager(app)

with open('seed.json', 'r') as json_file:
  seed_data = json.load(json_file)

@manager.command
def seed():
  print("Seeding the database...")

  try:
    mapped_seed_data = []

    for data in seed_data:
      if not data['close_date']:
        data['close_date'] = None
      data['case_text'] = re.sub(r'[\n\r\t]','',data['case_text'])
      data['embedding'] = np.array(extract_embeddings([data['case_text']])).tolist()[0]
      data['keywords'] = ast.literal_eval(data['keywords'])
      data['relations'] = ast.literal_eval(data['relations'])
      data['risk_factors'] = ast.literal_eval(data['risk_factors'])
      data['topic_verbs'] = ast.literal_eval(data['topic_verbs'])
      data['similar_cases'] = ast.literal_eval(data['similar_cases'])

      mapped_seed_data.append(Case(
        case_number = data['case_number'],
        case_text = data['case_text'],
        country = data['country'],
        open_date = data['open_date'],
        is_closed = data['is_closed'],
        close_date = data['close_date'],
        service = data['service'],
        summary = data['summary'],
        keywords = data['keywords'],
        relations = data['relations'],
        embedding = data['embedding'],
        risk_score = data['risk_score'],
        risk_factors = data['risk_factors'],
        topic_verbs = data['topic_verbs'],
        similar_cases = data['similar_cases']
      ))

    db.session.add_all(mapped_seed_data)
    db.session.commit()

    print("Database seeded with {} cases!".format(len(mapped_seed_data)))

  except Exception as e:
    print(str(e))


if __name__ == "__main__":
  manager.run()
