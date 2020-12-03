from wtforms import SubmitField, StringField, BooleanField, DateField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import datetime

class CaseForm(FlaskForm):
    case_text = TextAreaField('Case Text', description='Enter service(s) requested, background information and assessment (if any)')

    case_upload = FileField('File', description='Upload a case file or supplementary document', validators=[FileAllowed(['txt'],'txt file only')])

    submit = SubmitField('Submit')

class QueryForm(FlaskForm):
    case_number = StringField('Find a case by case number')

    open_date = DateField('Find cases that opened on or after this date', description='Please follow this format: YYYY-MM-DD', validators=[validators.Optional()])

    close_date = DateField('Find cases that closed on or before this date', description='Please follow this format: YYYY-MM-DD', validators=[validators.Optional()])

    country = StringField('Find cases where service is requested in this country')

    service = SelectField('Service Requested', choices=['', 'Child Protection', 'Children on the Move'], validate_choice=False)

    keywords = TextAreaField('Find cases that contain these words', description='Please separate words with a comma.')

    submit = SubmitField('Search')
