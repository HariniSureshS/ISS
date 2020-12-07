from wtforms import SubmitField, StringField, RadioField, BooleanField, DateField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import datetime
from flask_babel import lazy_gettext as _
class CaseForm(FlaskForm):
    case_text = TextAreaField(_('Case Text'), description=_('Enter service(s) requested, background information and assessment (if any)'))

    case_upload = FileField(_('File'), description=_('Upload a case file or supplementary document'), validators=[FileAllowed(['txt'],'txt file only')])

    submit = SubmitField(_('Submit'))

class QueryForm(FlaskForm):
    get_open_close = RadioField(choices=[[0, 'Show open cases only'], [1, 'Show closed cases only'], [2, 'Show both open and closed cases']], default=2)

    case_number = StringField('Show a case by case number')

    open_date = DateField('Show cases that opened on or after this date', description='Please follow this format: YYYY-MM-DD', validators=[validators.Optional()])

    close_date = DateField('Show cases that closed on or before this date, if closed', description='Please follow this format: YYYY-MM-DD', validators=[validators.Optional()])

    country = StringField('Show cases where service is requested in this country')

    service = SelectField('Show cases with the following service requested', choices=['', 'Child Protection', 'Children on the Move'], validate_choice=False)

    keywords = TextAreaField('Show cases that contain these words', description='Please separate words with a comma.')

    get_high_risk = BooleanField('Show high risk cases only', description='High risk cases have risk score of or over 0.75')

    submit = SubmitField('Search')
