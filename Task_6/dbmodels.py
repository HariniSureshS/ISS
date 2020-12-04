from app import db

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String())
    open_date = db.Column(db.Date())
    is_closed = db.Column(db.Boolean())
    close_date = db.Column(db.Date())
    country = db.Column(db.String())
    service = db.Column(db.String())
    case_text = db.Column(db.Text())
    embedding = db.Column(db.ARRAY(db.Float))
    risk_score = db.Column(db.Float())
    summary = db.Column(db.Text())
    keywords = db.Column(db.ARRAY(db.Text()))
    topic_word = db.Column(db.String())

    def __init__(
        self,
        case_number = None,
        open_date = None,
        is_closed = None,
        close_date = None,
        country = None,
        service = None,
        case_text = None,
        embedding = None,
        risk_score = None,
        summary = None,
        keywords = None,
        topic_word = None
    ):
        self.case_number = case_number
        self.open_date = open_date
        self.is_closed = is_closed
        self.close_date = close_date
        self.country = country
        self.service = service
        self.case_text = case_text
        self.embedding = embedding
        self.risk_score = risk_score
        self.summary = summary
        self.keywords = keywords
        self.topic_word = topic_word

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
            'embedding': self.embedding,
            'risk_score': self.risk_score,
            'summary': self.summary,
            'keywords': self.keywords,
            'topic_word': self.topic_word
        }
