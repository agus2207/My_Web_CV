# import numpy as np
# import pandas as pd
import json
# from datetime import datetime
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.GanttComponent import *
from utils.skills import *

dash.register_page(__name__, path='/', name='About Me')

# gantt_trabajo = GanttComponent(dash, df[df['Type'] == 'Work'], id_prefix='gantt-trabajo')
# gantt_educacion = GanttComponent(dash, df[df['Type'] == 'School'], id_prefix='gantt-educacion')

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
    dash.Input('tabs-example-graph', 'value'),
    dash.Input('shared-data-store', 'data')
)
def render_content(tab, json_data):
    if not json_data:
        return html.Div()
    data_dict = json.loads(json_data)
    if tab == 'tab-1':
        return html.Div([
            html.P("Contenido para 'About me' (similar a MY_INFO)"),
            html.A("Google", href="http://www.google.com", target="_blank")
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3("Education History"),
            html.P("A tour of my academic journey. This interactive timeline summarizes the institutions and programs that have shaped my knowledge, showcasing my key achievements and academic growth over time."),
            gantt_layout('2-chart', json.loads(data_dict['fig_edu']), '2-output-text')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3("My Professional Journey"),
            html.P("A tour of my professional history. This interactive timeline summarizes the companies and roles that have defined my career, showcasing my progress and contributions over time."),
            gantt_layout('1-chart', json.loads(data_dict['fig_work']), '1-output-text')
            # gantt_trabajo.get_layout()
        ])
    elif tab == 'tab-4':
        return skill_section(data_dict)
