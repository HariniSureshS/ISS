from app import db
import tensorflow_hub as hub
model = hub.load('https://tfhub.dev/google/universal-sentence-encoder/4')


class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.Text())
    open_date = db.Column(db.Date())
    is_closed = db.Column(db.Boolean())
    close_date = db.Column(db.Date())
    country = db.Column(db.String())
    service = db.Column(db.String())
    case_text = db.Column(db.Text())
    embeddings = db.Column(db.ARRAY(db.Float))
    embeddings_date = db.Column(db.Date())

    def __init__(self, case_number, open_date, is_closed, close_date, country, service, case_text, embeddings, embeddings_date):
        self.case_number = case_number
        self.open_date = open_date
        self.is_closed = is_closed
        self.close_date = close_date
        self.country = country
        self.service = service
        self.case_text = case_text
        self.embeddings = embeddings
        self.embeddings_date = embeddings.date

    def __repr__(self):
        return "<Case {}>".format(self.case_number)

    def serialize(self):
        return {
            'id': self.id,
            'case_number': self.case_number,
            'open_date': self.open_date,
            'is_closed': self.is_closed,
            'close_date': self.close_date,
            'country': self.country,
            'service': self.service,
            'case_text': self.case_text,
            'embeddings': self.embeddings,
            'embeddings_date': self.embeddings_date
        }
