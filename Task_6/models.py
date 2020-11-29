from app import db


class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.Text())
    case_text = db.Column(db.Text())
    embeddings = db.Column(db.ARRAY(db.Float))
    embeddings_date = db.Column(db.Date())

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
