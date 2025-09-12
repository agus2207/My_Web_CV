import dash
from dash import dcc, html
import dash_bootstrap_components as dbc # 👈 Importar DBC en la página

dash.register_page(__name__, path='/', name='About Me')

layout = dbc.Container( # 👈 Usar un contenedor en la página
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
            html.Img(src='assets/input_files/images/school/ipn.png', style={'width': '150px'}),
            html.H3("Gantt de Educación") # Aquí iría tu función display_interactive_gantt
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.Img(src='assets/input_files/images/experience/program.jpg', style={'width': '150px'}),
            html.H3("Gantt de Experiencia") # Aquí iría tu función display_interactive_gantt
        ])
