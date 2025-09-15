import dash
import numpy as np
import pandas as pd
from datetime import datetime
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.GanttComponent import *

dash.register_page(__name__, path='/', name='About Me')

today = datetime.now()
today_str = today.strftime('%Y-%m-%d')

df = pd.read_csv("assets/datasets/experience.csv", encoding="latin-1", low_memory=False)
df['Finish'] = np.where(df['Place'].str.contains('Digitas', case=False, na=False), today_str, df['Finish'])
df['Start_str'] = pd.to_datetime(df['Start'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
df['Finish_str'] = pd.to_datetime(df['Finish'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')

gantt_trabajo = GanttComponent(dash, df[df['Type'] == 'Work'], id_prefix='gantt-trabajo')
gantt_educacion = GanttComponent(dash, df[df['Type'] == 'School'], id_prefix='gantt-educacion')

layout = dbc.Container(
    html.Div(children=[
        html.H1("Hello there 👋"),
        html.H2("Thanks for stopping by!"),
        dcc.Tabs(id="tabs-example-graph", value='tab-1', children=[
            dcc.Tab(label="About me", value='tab-1'),
            dcc.Tab(label="Education", value='tab-2'),
            dcc.Tab(label="Experience", value='tab-3'),
            dcc.Tab(label="Skills", value='tab-4'),
            dcc.Tab(label="Other Projects", value='tab-5'),
            dcc.Tab(label="Hobbies", value='tab-6'),
        ]),
        html.Div(id='tabs-content-example-graph')
    ])
)

@dash.callback(
    dash.Output('tabs-content-example-graph', 'children'),
    dash.Input('tabs-example-graph', 'value')
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.P("Contenido para 'About me' (similar a MY_INFO)"),
            html.A("Google", href="http://www.google.com", target="_blank")
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3("My Education Timeline"),
            gantt_educacion.get_layout()
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3("My Experience Timeline"),
            gantt_trabajo.get_layout()
        ])
    elif tab == 'tab-4':
        data = {
            'categoria': [
                'Análisis de Datos', 'Análisis de Datos', 'Análisis de Datos',
                'Desarrollo Web', 'Desarrollo Web',
                'Automatización', 'Automatización',
                'Pruebas', 'Web Scraping', 'Web Scraping'
            ],
            'libreria': [
                'Pandas', 'Numpy', 'PySpark',
                'Django', 'Flask',
                'Selenium', 'Dash',
                'Pytest',
                'BeautifulSoup', 'openpyxl'
            ],
            'dominio': [90, 90, 75, 85, 90, 70, 80, 65, 75, 60] # Porcentaje o escala
        }

        df_librerias = pd.DataFrame(data)

        fig = px.treemap(
            df_librerias,
            path=[px.Constant('Librerías de Python'), 'categoria', 'libreria'],
            values='dominio',
            color='dominio',
            color_continuous_scale='bluyl',RdBu
            title='Dominio de Librerías de Python'
        )

        return html.Div([
            dcc.Graph(id="self.graph_id", figure=fig),
            html.Div(
                id="self.output_id",
                style={'margin-top': '20px', 'font-size': '18px'}
            )
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
