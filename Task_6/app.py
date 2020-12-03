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

risk_model = load_model('models/risk_0.189.h5')


@app.route('/')
def main_menu():
    print('Please select an option: (1) run models (2) query database.')
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
                           similar_cases=get_similar(case_text),
                           translation=translate(case_text))


def summarize(case_text):
    return case_text


def get_keywords(case_text):
    return 'hi'


def get_risk_score(case_text):
    score = risk_model.predict(np.expand_dims(x_test, axis=0))[0][0]
    # x_test risk score should be around 0.75
    # print(type(y_hat), y_hat)
    # <class 'numpy.float32'> 0.75826347
    return format(score, ".2f")


def get_similar(case_text):
    return extract_embeddings([case_text])


def translate(case_text):
    return 'trans'


@app.route('/query', methods=['GET', 'POST'])
def query_db():
    # get all cases (o)
    # get open cases
    # get closed cases; get closed cases that took less than 3 months
    # get case by id (o)
    # get cases by country
    # get cases by date range (start, end)
    # get cases by service requested
    # get cases whose risk_score is >= 0.75, in order

    # form input:
    # - get_all: Boolean (if True, get all cases)
    # - get_open: (radio) Boolean (if True, only get open cases)
    # - get_close: (radio) Boolean (if True, only get closed cases)
    # - case_id: Integer --> return one case or None
    # - country: String --> return all cases whose country equals to input
    # - start_date: Date
    # - end_date: Date
    # - service: String
    query_form = QueryForm()
    if request.method == 'POST' and query_form.validate_on_submit():
        if request.form['case_number'] != '':
            return redirect(url_for('get_case_by_number', case_number_=request.form['case_number']))

        return redirect(url_for('get_all_cases', params=request.form))
    else:
        return render_template('query.html', form=query_form)


# get all cases
@app.route('/allcases')
def get_all_cases():
    try:
        # if params['country'] != '':

        # if params['get_open']:

        # if params['get_close']:

        # if params[''] etc.


        # if no parameters are specified, get all cases
        cases = dbmodels.Case.query.all()
        return jsonify([case.serialize() for case in cases])
    except Exception as e:
        return str(e)


# get case by case_number
@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        case = dbmodels.Case.query.filter_by(case_number=case_number_).first()
        return jsonify(case.serialize())
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
