import pandas as pd
import plotly
import plotly.graph_objs as go
import json


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

