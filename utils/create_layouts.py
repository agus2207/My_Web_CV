import dash
import json
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px

def create_radar(df, title):
    fig = px.line_polar(
        df,
        r='domain',
        theta='name',
        line_close=True,
        markers=True,
        title=title,
        range_r=[0,100],
    )
    fig.update_traces(fill='toself')
    return fig

def create_map(df, title, constant):
    fig = px.treemap(
        df,
        path=[px.Constant(constant), 'category', 'name'],
        values='domain',
        color='domain',
        color_continuous_scale='rdylbu',#RdBu
        title=title
    )
    return fig

def create_bar(df, title):
    fig = px.bar(
        df,
        x='domain',
        y='name',
        orientation='h',
        title=title,
        range_x=[0, 100],
        text='domain',
        color='domain',
        color_continuous_scale=px.colors.sequential.Plasma
    )
    fig.update_layout(xaxis_title="Domain level (%)", yaxis_title="")
    return fig

def create_pie(df, title):
    fig = px.pie(
        df,
        values='domain',
        names='name',
        title=title,
        hole=.4
    )
    fig.update_traces(textinfo='label', showlegend=False)
    return fig

def create_timeline(df):
    fig = px.timeline(
        df,
        x_start="Start",
        x_end="Finish",
        y="Place",
        color="Place",
        custom_data=["Item", "Place", "Start_str", "Finish_str", "Description", "Imagen"]
    )
    fig.update_yaxes(autorange="reversed")
    return fig

def gantt_layout(id_gantt, fig, output_id):
    return html.Div([
        dcc.Graph(id={'type': 'gantt-chart', 'index': id_gantt}, figure=fig),
        html.Div(
            id={'type': 'gantt-output-text', 'index': id_gantt},
            style={'margin-top': '20px', 'font-size': '18px'}
        )
    ])

def skill_section(data_strorage):
    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3("Core Competencies"),
                    html.P("Take a look at my skills in a new light. These charts showcase my expertise in the abilities and technologies that define my professional work.")
                ])
            )
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='libraries', figure=json.loads(data_strorage['fig_li']))))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='planguages', figure=json.loads(data_strorage['fig_pl'])))),
            dbc.Col(html.Div(dcc.Graph(id='bi', figure=json.loads(data_strorage['fig_bi']))))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='apache', figure=json.loads(data_strorage['fig_apache'])))),
            dbc.Col(html.Div(dcc.Graph(id='sql', figure=json.loads(data_strorage['fig_sql']))))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='cloud', figure=json.loads(data_strorage['fig_cloud']))))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='agile', figure=json.loads(data_strorage['fig_agile'])))),
            dbc.Col(html.Div(dcc.Graph(id='tech', figure=json.loads(data_strorage['fig_tech']))))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='learning', figure=json.loads(data_strorage['fig_learning'])))),
            dbc.Col(html.Div(dcc.Graph(id='lan', figure=json.loads(data_strorage['fig_lan'])))),
            dbc.Col(html.Div(dcc.Graph(id='learning', figure=json.loads(data_strorage['fig_marketing']))))
        ]),
    ])
