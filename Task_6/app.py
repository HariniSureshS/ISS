#!bin/python
from flask import Flask, session, request, redirect, url_for, render_template, jsonify
from forms import CaseForm, QueryForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import numpy as np
import tensorflow as tf
import keras
from keras.models import load_model
from models.embedding_model import extract_embeddings
from models.abuse_types import abuse_types

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\x94\xf4\xb6Eo\xc4?Kia\x852\xbc\xe9S~\xb7\xd0\xb7#a\x93g\xb8',
    WTF_CSRF_TIME_LIMIT=None,
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/iss",
    SQLALCHEMY_ECHO= True)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)

from sample import x_test
import dbmodels
import datetime

risk_model = load_model('models/risk_0.189.h5')


@app.route('/')
def main_menu():
    print('Please select option: (1) run models on new case (2) query database.')
    return redirect('/models')


# form page to input a new case and test out ML models
@app.route('/models', methods=['GET', 'POST'])
def enter_case():
    case_form = CaseForm()
    if request.method == 'POST' and case_form.validate_on_submit():
        session['form'] = request.form
        file_data = request.files.get('case_upload')
        file_data.seek(0)
        content = file_data.read().decode('utf-8')
        session['file'] = content
        return redirect('/models/result')
    return render_template('case.html', form=case_form)


@app.route('/models/result')
def show_result():
    form_input = session['form']
    file_input = session['file']
    if file_input == "":
        case_text = form_input['case_text']
    else:
        case_text = file_input

    return render_template('result.html',
                           input=form_input,
                           summary=summarize(case_text),
                           keywords=get_keywords(case_text),
                           risk_score=get_risk_score(case_text),
                           abuse_types=get_abuse_types(case_text),
                           similar_cases=get_similar(case_text),
                           translation=translate(case_text))


def summarize(case_text):
    return 'summary'


def get_keywords(case_text):
    return 'hi'


def get_risk_score(case_text):
    text_embedding = extract_embeddings([case_text])
    score = risk_model.predict(text_embedding)[0][0]

    risk_level = None
    if score <= 0.35:
        risk_level = 'low'
    elif score >= 0.75:
        risk_level = 'high'
    else:
        risk_level = 'medium'

    return "This is a {} risk case, with the score of ".format(risk_level) + format(score, ".2f")


def get_abuse_types(case_text):
    return "Two top abuse types of this case are: " + abuse_types(case_text)[0] + ', ' + abuse_types(case_text)[1]


def get_similar(case_text):
    # extract_embedding's input must be a list containing a string
    return extract_embeddings([case_text])


def translate(case_text):
    return 'trans'


# form page to query cases from database
@app.route('/query', methods=['GET', 'POST'])
def query_db():
    query_form = QueryForm()
    if request.method == 'POST' and query_form.validate_on_submit():
        if request.form['case_number'] != '':
            return redirect(url_for('get_case_by_number', case_number_=request.form['case_number']))
        session['params']=request.form
        return redirect(url_for('get_all_cases'))
    else:
        return render_template('query.html', form=query_form)


@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        case = dbmodels.Case.query.filter_by(case_number=case_number_).first_or_404(description='There is no data with the following case_number: {}'.format(case_number_))
        return jsonify(case.serialize())
    except Exception as e:
        return str(e)


@app.route('/allcases')
def get_all_cases():
    params = session['params']
    try:
        Case = dbmodels.Case
        cases = Case.query

        if params['country']:
            cases = cases.filter_by(country=params['country'])

        if params['get_open_close'] == '0':
            cases = cases.filter_by(is_closed=False)
        elif params['get_open_close'] == '1':
            cases = cases.filter_by(is_closed=True)

        if params['open_date']:
            cases = cases.filter(Case.open_date >= params['open_date'])

        if params['close_date']:
            cases = cases.filter(Case.close_date >= params['close_date'])

        if params['service'] == 'Child Protection':
            cases = cases.filter_by(service='Child Protection')
        elif params['service'] == 'Children on the Move':
            cases = cases.filter_by(service='Children on the Move')

        # if params['keywords']:

        # if params['get_high_risk']:
        #     print('get high true')
        # #     cases = cases.filter(Case.risk_score >= 0.75)

        cases = cases.all()
        # print('found cases', str(cases))

        return jsonify([case.serialize() for case in cases])
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
