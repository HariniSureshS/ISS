from wtforms import SubmitField, StringField, BooleanField, DateField, TextAreaField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import datetime

class CaseForm(FlaskForm):
    case_number = StringField('Case Number')
    open_date = DateField('Case Open Date (YYYY-MM-DD)', default=datetime.datetime.today)
    is_closed = BooleanField('This is a closed case')
    close_date = DateField('Case Close Date (YYYY-MM-DD)', description='If case is closed', validators=[validators.Optional()])
    country = StringField('Country', description='Country where service is requested')
    case_text = TextAreaField('Case Text', description='Enter service(s) requested, background information and assessment (if any)')
    case_upload = FileField('File', description='Upload a case file or supplementary document', validators=[FileAllowed(['txt'],'txt file only')])
    submit = SubmitField('Submit')
