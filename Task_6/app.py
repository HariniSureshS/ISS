#!bin/python
from flask import Flask, session, request, redirect, url_for, render_template, jsonify
from forms import CaseForm, QueryForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
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
from models.abuse_types import abuse_types
from load import load_data
from settings import *

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=os.urandom(32),
    WTF_CSRF_TIME_LIMIT=None)
Bootstrap(app)

from sample import x_test
import datetime

#risk_model = load_model(MODEL_DIR)
data = load_data()

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
    return case_text


def get_keywords(case_text):
    return 'hi'


def get_risk_score(case_text):
    #score = risk_model.predict(np.expand_dims(x_test, axis=0))[0][0]
    # x_test risk score should be around 0.75
    # print(type(y_hat), y_hat)
    # <class 'numpy.float32'> 0.75826347
    score =0.75
    return format(score, ".2f")


def get_abuse_types(case_text):
    return "Two top abuse types of this case are: " + str(abuse_types(case_text))


def get_similar(case_text):
    # extract_embedding's input must be a list containing a string
    #return extract_embeddings([case_text])
    return 0.030634345565


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


# def get_case_by_number(case_number_):
#     try:
#         case = dbmodels.Case.query.filter_by(case_number=case_number_).first_or_404(description='There is no data with the following case_number: {}'.format(case_number_))
#         return jsonify(case.serialize())
#     except Exception as e:
#         return str(e)

# def get_all_cases():
#     params = session['params']
#     try:
#         Case = dbmodels.Case
#         cases = Case.query

#         if params['country']:
#             cases = cases.filter_by(country=params['country'])

#         if params['get_open_close'] == '0':
#             cases = cases.filter_by(is_closed=False)
#         elif params['get_open_close'] == '1':
#             cases = cases.filter_by(is_closed=True)

#         if params['open_date']:
#             full = params['open_date'].split('-')
#             year = int(full[0])
#             month = int(full[1])
#             day = int(full[2])
#             start = datetime.date(year, month, day)

#             cases = cases.filter(Case.open_date >= start)

#         if params['close_date']:
#             full = params['close_date'].split('-')
#             year = int(full[0])
#             month = int(full[1])
#             day = int(full[2])
#             end = datetime.date(year, month, day)

#             cases = cases.filter(Case.close_date >= end)

#         if params['service'] == 'Child Protection':
#             cases = cases.filter_by(service='Child Protection')
#         elif params['service'] == 'Children on the Move':
#             cases = cases.filter_by(service='Children on the Move')

#         # if params['keywords']:

#         # if params['get_high_risk']:
#         #     print('get high true')
#         # #     cases = cases.filter(Case.risk_score >= 0.75)

#         cases = cases.all()
#         # print('found cases', str(cases))

#         #return jsonify([case.serialize() for case in cases])
#         df =pd.DataFrame.from_records([case.serialize() for case in cases])
#         graph = create_plot(df)
#         return render_template('cases.html', plot=graph)
#     except Exception as e:
#         return str(e)


@app.route('/case/number/<case_number_>')
def get_case_by_number(case_number_):
    try:
        filter = data["case_number"] == case_number_
        case = data.where(filter)
        if case.shape[0] > 0:
            graph,graph1,_ = create_plot(case)
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

        graph,graph1,graph2 = create_plot(cases)
        return render_template('cases.html', plot=graph,plot1=graph1,plot2=graph2)
    except Exception as e:
        return str(e)


def create_plot(df):
    #N = 40
    #x = np.linspace(0, 1, N)
    #y = np.random.randn(N)
    #df = pd.DataFrame({'x': x, 'y': y}) 
    freq = df["case_text"].str.split(expand=True).stack().value_counts()[:50]
    bar = [
        go.Bar(
            x=freq.index, 
            y=freq.values,
            marker_color='lightcoral',
            text=freq.values,
            textposition='auto'
        )
    ]
    graph =go.Figure(bar)
    graph.update_layout(
        title='Frequency Word Count',
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Frequency Word Count',
            titlefont_size=18,
            tickfont_size=16
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255,255,255,0)',
            bordercolor='rgba(255,255,255,0)'
        ),
        barmode='group',
        xaxis_tickangle=-45,
        bargap=0.15,
        bargroupgap=0.1
    )

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

    colors =["#FA2B0A","#9B1803","#861604","#651104","#570303","#F9F9F5","#FAFAE6","#FCFCCB","#FCFCAE","#FCF1AE","#FCEA7D","#FCD97D",
             "#FCCE7D","#FE5E19","#FA520A","#FCC07D","#FEB562","#F9A648","#F98E48","#FD8739","#FE7519",
             ]
    world =go.Figure(data=go.Choropleth(
        locationmode = "country names",
        locations = new_frame['Country'],
        z = new_frame['Totals'],
        text = new_frame['Country'],
        colorscale ='Blues',
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
    graphJ = json.dumps(graph, cls=plotly.utils.PlotlyJSONEncoder)
    tableJ = json.dumps(table, cls=plotly.utils.PlotlyJSONEncoder)
    worldJ = json.dumps(world, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJ,tableJ,worldJ

if __name__ == '__main__':
    app.run(debug=True)
