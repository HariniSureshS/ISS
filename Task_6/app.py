#!bin/python
from flask import Flask, session, request, redirect, url_for, render_template
from form import CaseForm
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

@app.route('/', methods=['GET', 'POST'])
def enter_case():
    case_form = CaseForm()
    if request.method == 'POST' and case_form.validate_on_submit():
        session['form'] = request.form
        file_data = request.files.get('case_upload')
        file_data.seek(0)
        content = file_data.read().decode('utf-8')
        session['file'] = content
        return redirect('/result')
    return render_template('case.html', form=case_form)

@app.route('/result')
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
    y_hat = risk_model.predict(np.expand_dims(x_test, axis=0))[0][0]
    # x_test risk score should be around 0.75
    # print(type(y_hat), y_hat)
    # <class 'numpy.float32'> 0.75826347
    return y_hat


def get_similar(case_text):
    return extract_embeddings([case_text])


def translate(case_text):
    return 'trans'


if __name__ == '__main__':
    app.run(debug=True)
