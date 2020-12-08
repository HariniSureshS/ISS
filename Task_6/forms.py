from wtforms import SubmitField, StringField, RadioField, BooleanField, DateField, TextAreaField, SelectField, validators
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
import datetime
from flask_babel import lazy_gettext as _

class CaseForm(FlaskForm):
    case_text = TextAreaField(_('Case Text'), description=_('Enter service(s) requested, background information and assessment (if any)'))

    case_upload = FileField(_('File'), description=_('Upload a case file or supplementary document'), validators=[FileAllowed(['txt'],_('txt file only'))])

    submit = SubmitField(_('Submit'))

class QueryForm(FlaskForm):
    get_open_close = RadioField(choices=[[0, _('Show open cases only')], [1, _('Show closed cases only')], [2, _('Show both open and closed cases')]], default=2)

    case_number = StringField(_('Show a case by case number'))

    open_date = DateField(_('Show cases that opened on or after this date'), description=_('Please follow this format: YYYY-MM-DD'), validators=[validators.Optional()])

    close_date = DateField(_('Show cases that closed on or before this date, if closed'), description=_('Please follow this format: YYYY-MM-DD'), validators=[validators.Optional()])

    country = StringField(_('Show cases where service is requested in this country'))

    service = SelectField(_('Show cases where the following service is requested'), choices=['', _('Child Protection'), _('Children on the Move')], validate_choice=False)

    keywords = TextAreaField(_('Show cases that contain these words'), description=_('Please separate words with a comma'))

    get_high_risk = BooleanField(_('Show high risk cases only'), description=_('High risk cases have risk score of or over 0.75'))

    submit = SubmitField(_('Search'))
