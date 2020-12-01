import app
import tensorflow_hub as hub
model = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')


class Case(app.db.Model):
    __tablename__ = 'cases'

    id = app.db.Column(app.db.Integer, primary_key=True)
    case_number = app.db.Column(app.db.Text())
    case_text = app.db.Column(app.db.Text())
    embeddings = app.db.Column(app.db.ARRAY(app.db.Float))
    embeddings_date = app.db.Column(app.db.Date())

    def __init__(self, case_number, case_text, embeddings, embeddings_date):
        self.case_number = case_number
        self.case_text = case_text
        self.embeddings = embeddings
        self.embeddings_date = embeddings.date

    def __repr__(self):
        return "<Case {}>".format(self.case_number)

    def serialize(self):
        return {
            'id': self.id,
            'case_number': self.case_number,
            'case_text': self.case_text,
            'embeddings': self.embeddings,
            'embeddings_date': self.embeddings_date
        }

def extract_embeddings(query):
    return model(query)
