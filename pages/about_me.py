import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.constants import MY_DATA
from utils.create_layouts import *

dash.register_page(__name__, path='/', name='About Me')

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
    dash.Output({'type': 'gantt-output-text', 'index': dash.MATCH}, 'children'),
    dash.Input({'type': 'gantt-chart', 'index': dash.MATCH}, 'clickData')
)
def display_click_data(clickData):
    if clickData is None:
        return "Click on a bar to view the information."

    punto = clickData['points'][0]
    tarea, place, inicio, fin, descripcion, image = punto['customdata']

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Img(src=image, style={'width': '150px'})
                ]),
                width=2
            ),
            dbc.Col(
                html.Div([
                    html.H3(f"{place}"),
                    html.P(f"{tarea}"),
                    html.P(f"Start date: {inicio}"),
                    html.P(f"End Date: {fin}") if "Digitas" not in place else html.P(f"End Date: Present"),
                ]),
                width=8
            ),
        ]),
        html.P(f"\n\n"),
        dcc.Markdown(children=descripcion)
    ])

@dash.callback(
    dash.Output('tabs-content-example-graph', 'children'),
    dash.Input('tabs-example-graph', 'value'),
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            html.P("Contenido para 'About me' (similar a MY_INFO)"),
            html.A("Google", href="http://www.google.com", target="_blank")
        ])
    elif tab == 'tab-2':
        return html.Div([
            html.H3("Education History"),
            html.P("A tour of my academic journey. This interactive timeline summarizes the institutions and programs that have shaped my knowledge, showcasing my key achievements and academic growth over time."),
            gantt_layout('eductation-chart', MY_DATA['fig_edu'], 'eductation-output-text')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3("My Professional Journey"),
            html.P("A tour of my professional history. This interactive timeline summarizes the companies and roles that have defined my career, showcasing my progress and contributions over time."),
            gantt_layout('work-chart', MY_DATA['fig_work'], 'work-output-text')
        ])
    elif tab == 'tab-4':
        return skill_section(MY_DATA)
