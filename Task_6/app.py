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


# form page to query cases from database
@app.route('/query', methods=['GET', 'POST'])
def query_db():
    # form input:
    # - get_both_open_and_close: (radio) Boolean (if True, get all cases)
    # - get_open: (radio) Boolean (if True, only get open cases)
    # - get_close: (radio) Boolean (if True, only get closed cases)
    # - country: String --> return all cases whose country equals to input
    # - date_range: (check) Boolean (if True, validate start_date and end_date)
    # - start_date: Date (if date_range and start_date != '': start = start_date, else: start = None)
    # - end_date: Date
    # - service: String
    # - get_high_risk: Boolean
    query_form = QueryForm()
    if request.method == 'POST' and query_form.validate_on_submit():
        if request.form['case_number'] != '':
            return redirect(url_for('get_case_by_number', case_number_=request.form['case_number']))
        return redirect(url_for('get_all_cases', params=request.form))
    else:
        return render_template('query.html', form=query_form)


@app.route('/allcases')
def get_all_cases():
    try:
        find_cases = dbmodels.Case.query
        # if params['country'] != '':

        # if params['get_open_only']:

        # if params['get_close_only']:

        # if params['date_range']:
            # User.query.order_by(User.username).all()

        # if params['service']:

        # if params['get_high_risk']:
            # get cases whose risk_score is >= 0.75, in order


        # if no parameters are specified, get all cases
        cases = find_cases.all()
        return jsonify([case.serialize() for case in cases])
    except Exception as e:
        return str(e)


@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        case = dbmodels.Case.query.filter_by(case_number=case_number_).first_or_404(description='There is no data with the following case_number: {}'.format(case_number_))
        return jsonify(case.serialize())
    except Exception as e:
        return str(e)


if __name__ == '__main__':
    app.run(debug=True)
