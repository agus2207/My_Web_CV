import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime

def create_radar(df, title):
    fig = px.line_polar(
        df,
        r='domain',
        theta='name',
        line_close=True,
        markers=True,
        title=title,
        range_r=[0,100], # Define el rango para que la escala sea clara
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
        orientation='h', # Barras horizontales
        title=title,
        range_x=[0, 100], # Asegura que la barra vaya de 0 a 100
        text='domain', # Muestra el valor en la barra
        color='domain', # Colorea según el nivel de dominio
        color_continuous_scale=px.colors.sequential.Plasma # Escala de color
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

def skill_section():
    df = pd.read_csv("assets/datasets/skills.csv", encoding="latin-1", low_memory=False)
    fig_pl = create_radar(df[df['Type'] == 'Programming Languages'], 'Programming Languages Domain')
    fig_bi = create_bar(df[df['Type'] == 'BI'], 'BI Domain')
    fig_li = create_map(df[df['Type'] == 'Libraries'], 'Python Libraries Domain', 'Python Libraries')
    fig_apache = create_pie(df[df['Type'] == 'Apache'], 'Apache Knowleadge')
    fig_sql = create_radar(df[df['Type'] == 'DBMS'], 'DBMS Domain')
    fig_cloud = create_map(df[df['Type'] == 'Cloud'], 'Cloud Computing Domain', 'Cloud Computing')
    fig_learning = create_pie(df[df['Type'] == 'Learning'], 'Tech Learning')
    fig_tech = create_bar(df[df['Type'] == 'Tech'], 'Tech Knowleadge')
    fig_agile = create_pie(df[df['Type'] == 'Agile'], 'Known Agile Methodologies')
    fig_lan = create_bar(df[df['Type'] == 'Languages'], 'Spoken Languages')
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
            dbc.Col(html.Div(dcc.Graph(id='libraries', figure=fig_li)))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='planguages', figure=fig_pl))),
            dbc.Col(html.Div(dcc.Graph(id='bi', figure=fig_bi)))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='apache', figure=fig_apache))),
            dbc.Col(html.Div(dcc.Graph(id='sql', figure=fig_sql)))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='cloud', figure=fig_cloud)))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='agile', figure=fig_agile))),
            dbc.Col(html.Div(dcc.Graph(id='tech', figure=fig_tech)))
        ]),
        dbc.Row([
            dbc.Col(html.Div(dcc.Graph(id='lan', figure=fig_lan))),
            dbc.Col(html.Div(dcc.Graph(id='learning', figure=fig_learning)))
        ]),
    ])


'''
 ['aggrnyl', 'armyrose', 'balance','bluyl','darkmint'
             'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',
             'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',
             'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',
             'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',
             'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
             'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',
             'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',
             'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',
             'ylorrd']
'''
