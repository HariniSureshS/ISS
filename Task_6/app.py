#!bin/python
from flask import Flask, session, request, redirect, url_for, render_template, jsonify
from forms import CaseForm, QueryForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel,_
from sqlalchemy import or_, func
from flask_migrate import Migrate
import datetime
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import load_model
import json
import os
import pandas as pd
import plotly
import plotly.graph_objs as go
from models.embedding_model import extract_embeddings
from models.summarizer import get_summarizer
from models.abuse_types import abuse_types
from models.keyword_extractor import KeywordExtractor
from models.risk_factors import get_risk_factors
from flask_wtf.csrf import CsrfProtect

from load import load_data
from settings import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.urandom(32),
    WTF_CSRF_TIME_LIMIT=None)
app.config['BABEL_TRANSLATION_DIRECTORIES'] = TRANS_DIR
babel = Babel(app)
LANGUAGES = {
    'en' : 'English',
    'fr' : 'French',
    'de' : 'German',
    'zh' : 'Chinese',
    'ko' : 'Korean',
    'id' : 'Indonesian'
}
CsrfProtect(app)
Bootstrap(app)

#risk_model = load_model(MODEL_DIR)
data = load_data()

@app.route('/')
def main_menu():
    session.clear()
    return render_template('main.html')


# form page to input a new case and test out ML models
@app.route('/models', methods=['GET', 'POST'])
def enter_case():
    session.clear()
    case_form = CaseForm()
    if request.method == 'POST' and case_form.validate_on_submit():
            session['form'] = request.form
            file_data = request.files.get('case_upload')
            if file_data:
                file_data.seek(0)
                content = file_data.read().decode('utf-8')
                session['file'] = content
            elif not request.form['case_text']:
                return render_template('case.html', form=case_form)
            return redirect('/models/result')
    return render_template('case.html', form=case_form)



@app.route('/<page>/language/<language>')
def set_language(page=None, language=None):
    session['language'] = language
    print(page)
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
        print(language)
        return language
    return request.accept_languages.best_match(LANGUAGES.keys())



@app.context_processor
def inject_conf_var():
    return dict(
        AVAILABLE_LANGUAGES=LANGUAGES,
        CURRENT_LANGUAGE=session.get('language', request.accept_languages.best_match(LANGUAGES.keys())))


@app.route('/models/result')
def show_result():

    form_input = None
    file_input = None

    if 'form' in session.keys():
        form_input = session['form']

    if 'file' in session.keys():
        file_input = session['file']

    if file_input:
        case_text = file_input
    else:
        case_text = form_input['case_text']

    return render_template('result.html',
                           input=case_text,
                           summary=summarize(case_text),
                           keywords=get_keywords(case_text),
                           risk_score=get_risk_score(case_text),
                           abuse_types=get_abuse_types(case_text),
                           similar_cases=get_similar(case_text),
                           translation=translate(case_text))


def summarize(case_text):
    #return get_summarizer(case_text)
    return 'hi'


def get_keywords(case_text):
    extractor = KeywordExtractor()
    prep_text = extractor.preprocess_text(case_text)
    keywords = list(set(extractor.keyword_extraction(prep_text)))
    return keywords


def get_risk_score(case_text):
    #text_embedding = extract_embeddings([case_text])
    #score = risk_model.predict(text_embedding)[0][0]
    score =0.69

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
    # extract_embedding's input must be a list containing a string
    #return extract_embeddings([case_text])
    return 0.030634345565


def translate(case_text):
    print('Hi')
    # form_input = session['form']
    # if form_input['from_language']!= form_input['to_language']:
    #     return get_translation(case_text,
    #                            form_input['from_language'],
    #                            form_input['to_language'])
    # return case_text



# form page to query cases from database
@app.route('/query', methods=['GET', 'POST'])
def query_db():
    session.clear()
    query_form = QueryForm()
    if request.method == 'POST' and query_form.validate_on_submit():
        if request.form['case_number'] != '':
            return redirect(url_for('get_case_by_number', case_number_=request.form['case_number']))
        session['params']=request.form
        return redirect(url_for('get_all_cases'))
    else:
        return render_template('query.html', form=query_form)



# def get_case_by_number(case_number_):
#     try:
#         case = dbmodels.Case.query.filter_by(case_number=case_number_).first_or_404(description='There is no data with the following case_number: {}'.format(case_number_))
#         return jsonify(case.serialize())
#     except Exception as e:
#         return str(e)



# def get_all_cases():
    
#     params = {}
#     if 'params' in session.keys():
#         params = session['params']

#     try:
#         Case = dbmodels.Case
#         cases = Case.query
        
#         ##this is if someone clicks on "View all cases" link directly
#         if(len(params)==0):
#             return jsonify([case.serialize() for case in cases.all()])

#         if params['country']:
#             cases = cases.filter_by(country=params['country'])

#         if params['get_open_close'] == '0':
#             cases = cases.filter_by(is_closed=False)
#         elif params['get_open_close'] == '1':
#             cases = cases.filter_by(is_closed=True)

#         if params['open_date']:
#             cases = cases.filter(Case.open_date >= params['open_date'])

#         if params['close_date']:
#             cases = cases.filter(Case.close_date >= params['close_date'])

#         if params['service'] == 'Child Protection':
#             cases = cases.filter_by(service='Child Protection')
#         elif params['service'] == 'Children on the Move':
#             cases = cases.filter_by(service='Children on the Move')

#         if params['keywords']:
#             keywords = params['keywords'].split(",")
#             for keyword in keywords:
#                 keyword = keyword.strip().lower()
#             cases = cases.filter(or_(func.lower(Case.case_text).contains(word) for word in keywords))

#         if 'get_high_risk' in params:
#             cases = cases.filter(Case.risk_score >= 0.75)

#         cases = cases.all()
#         print("Total of {} cases were found!".format(len(cases)))

#         #return jsonify([case.serialize() for case in cases])
#         df =pd.DataFrame.from_records([case.serialize() for case in cases])
#         _,_,graph = create_plot(df)
#         return render_template('cases.html', plot=graph)
#     except Exception as e:
#         return str(e)


@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        filter = data["case_number"] == case_number_
        case = data.where(filter)
        if case.shape[0] > 0:
            graph,graph1,_,_ = create_plot(case)
            return render_template('cases.html', plot=graph,plot1=graph1)

        return jsonify({case_number_:"There is no data with the following case_number"})
    except Exception as e:
        return str(e)


@app.route('/allcases')
def get_all_cases():
    cases = data
    try:
        if session.get('params') is not None:
            params = session['params']       
            if params['country']:
                filter = cases["country"] == params['country']
                cases.where(filter,inplace=True)

            if params['get_open_close'] == '0':
                filter = cases["is_closed"] == False
                cases.where(filter,inplace=True)
            elif params['get_open_close'] == '1':
                filter = cases["is_closed"] == True
                cases.where(filter,inplace=True)

            if params['open_date']:
                full = params['open_date'].split('-')
                year = int(full[0])
                month = int(full[1])
                day = int(full[2])
                start = datetime.date(year, month, day)

                filter = cases["open_date"] >= start
                cases.where(filter,inplace=True)

            if params['close_date']:
                full = params['close_date'].split('-')
                year = int(full[0])
                month = int(full[1])
                day = int(full[2])
                end = datetime.date(year, month, day)

                filter = cases["close_date"] <= end
                cases.where(filter,inplace=True)


            if params['service'] == 'Child Protection':
                filter = cases["service"] == 'Child Protection'
                cases.where(filter,inplace=True)
            elif params['service'] == 'Children on the Move':
                filter = cases["service"] == 'Children on the Move'
                cases.where(filter,inplace=True)

            if params['keywords']:
                keywords = params['keywords'].split(",")
                for keyword in keywords:
                    keyword = keyword.strip().lower()
                #cases = cases.filter(or_(func.lower(Case.case_text).contains(word) for word in keywords))

            if 'get_high_risk' in params:
                filter = cases["risk_score"] >= 0.75
                cases.where(filter,inplace=True)

        graph,graph1,graph2,graph3 = create_plot(cases)
        return render_template('cases.html', plot=graph,plot1=graph1,plot2=graph2,plot3=graph3)
    except Exception as e:
        return str(e)


def create_plot(df):
    # freq = df["case_text"].str.split(expand=True).stack().value_counts()[:50]
    # bar = [
    #     go.Bar(
    #         x=freq.index, 
    #         y=freq.values,
    #         marker_color='lightcoral',
    #         text=freq.values,
    #         textposition='auto'
    #     )
    # ]
    # graph =go.Figure(bar)
    # graph.update_layout(
    #     title='Frequency Word Count',
    #     xaxis_tickfont_size=14,
    #     yaxis=dict(
    #         title='Frequency Word Count',
    #         titlefont_size=18,
    #         tickfont_size=16
    #     ),
    #     legend=dict(
    #         x=0,
    #         y=1.0,
    #         bgcolor='rgba(255,255,255,0)',
    #         bordercolor='rgba(255,255,255,0)'
    #     ),
    #     barmode='group',
    #     xaxis_tickangle=-45,
    #     bargap=0.15,
    #     bargroupgap=0.1
    # )

    dfObj= df.head(8)
    table =go.Figure([go.Table(
         header=dict(
             values=dfObj.columns,
             font=dict(size=12),
             align="left"
         ),
         cells=dict(
             values=[dfObj[k].tolist() for k in dfObj.columns],
             align="left"
         )
       )
    ])

    table.update_layout(
        autosize=True
    )
    total_cases =df['country'].value_counts().sort_index().values.tolist()

    countries = df['country'].tolist()
    countries =list(set(countries))
    countries.sort()

    new_frame = pd.DataFrame(list(zip(countries,total_cases)),
                     columns=['Country','Totals'])

    world =go.Figure(data=go.Choropleth(
        locationmode = "country names",
        locations = new_frame['Country'],
        z = new_frame['Totals'],
        text = new_frame['Country'],
        colorscale ='Viridis',
        autocolorscale=False,
        reversescale=False,
        marker_line_color='darkgray',
        marker_line_width=0.5,
        colorbar_title ='Reported Cases'
    ))


    world.update_layout(
        title_text='Reported Iss Cases',
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    data_df = df.groupby('service').agg({'case_number':'count'})
    labels = list(data_df.index.values)
    values = data_df['case_number']
    fig = go.Figure(data=[go.Pie(labels=labels, values=values,hole=.5)])


    df['month'] = pd.to_datetime(df["open_date"]).dt.strftime('%B')

    data_m =df.groupby('month').agg({'case_number':'count'})
    labels_m = list(data_m.index.values)
    values_m = data_m['case_number']
    fig1 = go.Figure(data=[go.Pie(labels=labels_m, values=values_m,hole=.5)])

    fig1.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20)

    tableJ = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    worldJ = json.dumps(world, cls=plotly.utils.PlotlyJSONEncoder)
    figS = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    figM = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)

    return worldJ,tableJ,figS,figM

if __name__ == '__main__':
    app.run(debug=True)
