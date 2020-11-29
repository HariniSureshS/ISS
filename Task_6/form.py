from wtforms import SubmitField, StringField, TextAreaField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed


class CaseForm(FlaskForm):
    case_number = StringField('Case Number')
    case_text = TextAreaField('Case Text')
    case_upload = FileField('File',validators=[FileAllowed(['txt'],'txt file only')])
    submit = SubmitField('Submit')
