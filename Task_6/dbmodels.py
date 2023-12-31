from app import db

class Case(db.Model):
    __tablename__ = 'cases'

    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String())
    open_date = db.Column(db.String())
    is_closed = db.Column(db.Boolean())
    close_date = db.Column(db.String())
    country = db.Column(db.String())
    service = db.Column(db.String())
    case_text = db.Column(db.Text())
    embedding = db.Column(db.ARRAY(db.Float()))
    risk_score = db.Column(db.Float())
    risk_factors = db.Column(db.ARRAY(db.String()))
    summary = db.Column(db.Text())
    keywords = db.Column(db.ARRAY(db.Text()))
    relations = db.Column(db.ARRAY(db.Text()))
    topic_verbs = db.Column(db.ARRAY(db.String()))
    similar_cases = db.Column(db.ARRAY(db.String()))

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
        risk_factors = None,
        summary = None,
        keywords = None,
        relations = None,
        topic_verbs = None,
        similar_cases = None
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
        self.risk_factors = risk_factors
        self.summary = summary
        self.keywords = keywords
        self.relations = relations
        self.topic_verbs = topic_verbs
        self.similar_cases = similar_cases

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
            'risk_factors': self.risk_factors,
            'summary': self.summary,
            'keywords': self.keywords,
            'relations': self.relations,
            'topic_verbs': self.topic_verbs,
            'similar_cases': self.similar_cases
        }
