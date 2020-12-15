#!bin/python
from flask import Flask, session, request, redirect, url_for, render_template
from forms import CaseForm, QueryForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel, _
from sqlalchemy import or_, func
from flask_migrate import Migrate
import json
import datetime
import pandas as pd
import plotly
import plotly.graph_objs as go
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from models.embedding_model import extract_embeddings
from models.summarizer import get_summary
from models.abuse_types import abuse_types
from models.keyword_extractor import KeywordExtractor
from models.relation_extractor import get_entity_pairs
from models.similar_cases import get_similar_cases
from models.risk_factors import get_risk_factors
from flask_wtf.csrf import CSRFProtect
from textConverters import convert_pdf_to_txt
from textConverters import doc_to_txt
import os

risk_model = load_model('models/risk_0.189.h5')

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\x94\xf4\xb6Eo\xc4?Kia\x852\xbc\xe9S~\xb7\xd0\xb7#a\x93g\xb8',
    WTF_CSRF_TIME_LIMIT=None,
    SQLALCHEMY_DATABASE_URI="postgresql://postgres:postgres@localhost:5432/iss",
    SQLALCHEMY_ECHO= True)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = './translations'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
babel = Babel(app)
LANGUAGES = {
    'en' : 'English',
    'fr' : 'French',
    'de' : 'German',
    'zh' : 'Chinese',
    'ko' : 'Korean',
    'id' : 'Indonesian'
}
CSRFProtect(app)
Bootstrap(app)

import dbmodels

@app.route('/')
def main_menu():
    session.pop('params', None)
    return render_template('main.html')


# form page to input a new case and test out ML models
@app.route('/models', methods=['GET', 'POST'])
def enter_case():
    session.pop('params', None)
    case_form = CaseForm()
    if request.method == 'POST' and case_form.validate_on_submit():
            session['form'] = request.form
            file_data = request.files.get('case_upload')
            
            if 'txt' in file_data.filename:
                file_data.save('./temp.txt')                
                session['file'] = 'txt'
            
            elif 'pdf' in file_data.filename:
                file_data.save('./temp.pdf')
                session['file'] = 'pdf'
                
            elif 'doc' in file_data.filename:
                file_data.save('./temp.doc')
                session['file'] = 'doc'
                
            elif not request.form.get('case_text', None):
                return render_template('models.html', form=case_form)
            return redirect('/models/result')
    return render_template('models.html', form=case_form)


@app.route('/<page>/language/<language>')
def set_language(page=None, language=None):
    session['language'] = language
    if page == 'models':
        return redirect(url_for('enter_case'))
    elif page == 'query':
        return redirect(url_for('query_db'))


@babel.localeselector
def get_locale():
    try:
        language = session['language']
    except KeyError:
        language = None
    if language is not None:
        return language
    return request.accept_languages.best_match(LANGUAGES.keys())


@app.context_processor
def inject_conf_var():
    return dict(
        AVAILABLE_LANGUAGES=LANGUAGES,
        CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(LANGUAGES.keys())))


@app.route('/models/result')
def show_result():
    session.pop('params', None)

    form_input = None
    file_input = None

    if 'form' in session.keys():
        form_input = session['form']

    if 'file' in session.keys():
        file_input = session['file']

    if file_input == 'pdf':
        case_text = convert_pdf_to_txt('./temp.pdf')
        os.remove('./temp.pdf')
    elif file_input == 'txt':
        case_text = open('./temp.txt').read()
        os.remove('./temp.txt')
    elif file_input == 'doc':
        case_text = doc_to_txt('./temp.doc')
        os.remove('./temp.doc')
        
    else:
        case_text = form_input['case_text']

    headers = ['Case No.', 'Case Summary', 'Country', 'Status', 'Risk Score']

    return render_template('models_result.html',
                           input=case_text,
                           summary=summarize(case_text),
                           keywords=get_keywords(case_text),
                           relations=get_relations(case_text),
                           risk_score=get_risk_score(case_text),
                           abuse_types=get_abuse_types(case_text),
                           similar_cases=get_similar(case_text),
                           headers=headers)


def summarize(case_text):
    return get_summary(case_text)


def get_keywords(case_text):
    extractor = KeywordExtractor()
    prep_text = extractor.preprocess_text(case_text)
    keywords = list(set(extractor.keyword_extraction(prep_text)))
    return keywords


def get_relations(case_text):
    relations = get_entity_pairs(case_text)
    if not len(relations):
        return "No entity relations found"
    else:
        return relations


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

    risk_words = get_risk_factors(case_text)

    return "This is a {} risk case, with the score of ".format(risk_level) + format(score, ".2f") + ". Possible words that may have affected the risk score are: {}".format(risk_words)


def get_abuse_types(case_text):
    return "Two top abuse types of this case are: " + abuse_types(case_text)[0] + ', ' + abuse_types(case_text)[1]


def get_similar(case_text):
    user_embedding = extract_embeddings([case_text])

    try:
        cases = dbmodels.Case.query.all()
        serialized_cases = [case.serialize() for case in cases]
        return get_similar_cases(serialized_cases, user_embedding, top_n = 5)

    except Exception as e:
        return 'Error: ' + str(e)


# form page to query database
@app.route('/query', methods=['GET', 'POST'])
def query_db():
    session.pop('params', None)

    query_form = QueryForm()
    if request.method == 'POST' and query_form.validate_on_submit():
        if request.form['case_number'] != '':
            return redirect(url_for('get_case_by_number', case_number_ = request.form['case_number']))

        session['params'] = request.form
        return redirect(url_for('get_all_cases'))

    else:
        return render_template('query.html', form=query_form)


@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        case = dbmodels.Case.query.filter_by(case_number = case_number_).first_or_404(description = 'There is no data with the following case_number: {}'.format(case_number_))

        df = pd.DataFrame.from_records(cases)
        graph, graph1, graph2 = create_plot(df)

        return render_template('query_result.html',
                                all_found_cases = [case.serialize()],
                                num_cases = 1,
                                plot = graph,
                                plot1 = graph1,
                                plot2 = graph2)

    except Exception as e:
        return 'Error: ' + str(e)


@app.route('/allcases/<case_number_>')
def view_single_case(case_number_):
    try:
        case = dbmodels.Case.query.filter_by(case_number = "Case No. {}".format(case_number_)).first().serialize()

        relations = []
        for each in case['relations']:
            relations.append(each[0] + ' --> ' + each[1] + ' --> ' + each[2])
        case['relations'] = relations

        return render_template('single_case.html', case = case, enumerate = enumerate, len = len)

    except Exception as e:
        return 'Error: ' + str(e)


@app.route('/allcases')
def get_all_cases():
    params = session.get('params', {})

    try:
        Case = dbmodels.Case
        cases = Case.query

        if not params:
            cases = cases.all()
            cases = [case.serialize() for case in cases]
            num_cases = len(cases)

            df = pd.DataFrame.from_records(cases)
            graph, graph1, graph2 = create_plot(df)

            return render_template('query_result.html',
                                    all_found_cases = cases,
                                    num_cases = num_cases,
                                    plot = graph,
                                    plot1 = graph1,
                                    plot2 = graph2)

        if params['country']:
            cases = cases.filter_by(country = params['country'])

        if params['get_open_close']:
            if params['get_open_close'] == '0':
                cases = cases.filter_by(is_closed = False)
            elif params['get_open_close'] == '1':
                cases = cases.filter_by(is_closed = True)

        if params['open_date']:
            cases = cases.filter(Case.open_date >= params['open_date'])

        if params['close_date']:
            cases = cases.filter(Case.close_date >= params['close_date'])

        if params['service'] == 'Child Protection':
            cases = cases.filter_by(service = 'Child Protection')
        elif params['service'] == 'Children on the Move':
            cases = cases.filter_by(service = 'Children on the Move')

        if params['keywords']:
            keywords = params['keywords'].split(",")
            for keyword in keywords:
                keyword = keyword.strip().lower()
            cases = cases.filter(or_(func.lower(Case.case_text).contains(word) for word in keywords))

        if 'get_high_risk' in params:
            cases = cases.filter(Case.risk_score >= 0.75)

        cases = cases.all()
        cases = [case.serialize() for case in cases]
        num_cases = len(cases)

        df = pd.DataFrame.from_records(cases)
        graph, graph1, graph2 = create_plot(df)

        return render_template('query_result.html',
                                all_found_cases = cases,
                                num_cases = num_cases,
                                plot = graph,
                                plot1 = graph1,
                                plot2 = graph2)

    except Exception as e:
        return 'Error: ' + str(e)


def create_plot(df):
    total_cases = df['country'].value_counts().sort_index().values.tolist()

    countries = df['country'].tolist()
    countries = list(set(countries))
    countries.sort()

    new_frame = pd.DataFrame(list(zip(countries,total_cases)),
                     columns = ['Country','Totals'])

    world = go.Figure(data = go.Choropleth(
        locationmode = "country names",
        locations = new_frame['Country'],
        z = new_frame['Totals'],
        text = new_frame['Country'],
        colorscale ='Viridis',
        autocolorscale = False,
        reversescale = False,
        marker_line_color = 'darkgray',
        marker_line_width = 0.5,
        colorbar_title = 'Reported Cases'
    ))

    world.update_layout(
        title_text='Reported ISS Cases',
        geo = dict(
            showframe = False,
            showcoastlines = False,
            projection_type = 'equirectangular'
        )
    )

    data_df = df.groupby('service').agg({'case_number':'count'})
    labels = list(data_df.index.values)
    values = data_df['case_number']
    fig = go.Figure(data = [go.Pie(labels = labels, values = values, hole = .5)])

    fig.update_layout(
        title_text = 'Service Category'
    )

    df['month'] = pd.to_datetime(df["open_date"]).dt.strftime('%B')
    df["Month"] = pd.to_datetime(df["open_date"]).dt.month
    data_m = df.groupby(['Month','month']).agg({'case_number':'count'}).reset_index()
    labels_m = list(data_m['month'])
    values_m = data_m['case_number']

    bar = [
        go.Bar(
            x = labels_m,
            y = values_m,
            marker = dict(color=['aliceblue','plum','mistyrose','thistle','khaki',
                'beige','darksalmon','lightcyan','blanchedalmond','lightcoral',
                'lavender','lightblue']),
            text = values_m,
            textposition = 'auto'
        )
    ]

    fig1 = go.Figure(bar)
    fig1.update_layout(
        title = 'Monthly Cases',
        xaxis_tickfont_size = 14,
        yaxis = dict(
            title = 'Frequency of Cases',
            titlefont_size = 18,
            tickfont_size = 16
        ),
        legend = dict(
            x = 0,
            y = 1.0,
            bgcolor = 'rgba(255,255,255,0)',
            bordercolor = 'rgba(255,255,255,0)'
        ),
        barmode = 'group',
        xaxis_tickangle = -45,
        bargap = 0.15,
        bargroupgap = 0.1
    )

    worldJ = json.dumps(world, cls = plotly.utils.PlotlyJSONEncoder)
    figS = json.dumps(fig, cls = plotly.utils.PlotlyJSONEncoder)
    figM = json.dumps(fig1, cls = plotly.utils.PlotlyJSONEncoder)

    return worldJ, figS, figM


if __name__ == '__main__':
    app.run(debug = True)
