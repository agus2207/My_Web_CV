import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify
from utils.constants import MY_DATA, ABOUT_ME, MY_HOBBIES, IMAGE_STYLE
from utils.create_layouts import *

dash.register_page(__name__, path='/', name='About Me')

layout = dbc.Container(
    html.Div(children=[
        html.H1("Hello there 👋"),
        html.H2("Thanks for stopping by!"),
        html.P([
            html.B("Technical Details"),
            ": This dashboard is powered by the Python programming language and the Dash framework. Deployment is managed via Google Cloud infrastructure. View the complete source code here:",
            html.A(href="https://github.com/agus2207/My_Web_CV", target="_blank", children=[DashIconify(icon="mdi:github", color="black", height=20,)])
        ], style={'fontStyle': 'italic'}),
        dcc.Tabs(id="tabs", value='tab-1', children=[
            dcc.Tab(label="About me", value='tab-1'),
            dcc.Tab(label="Education", value='tab-2'),
            dcc.Tab(label="Experience", value='tab-3'),
            dcc.Tab(label="Skills", value='tab-4'),
            # dcc.Tab(label="Other Projects", value='tab-5'),
            dcc.Tab(label="Hobbies", value='tab-6'),
        ]),
        html.Div(id='tabs-content')
    ])
)

@dash.callback(
    dash.Output({'type': 'gantt-output-text', 'index': dash.MATCH}, 'children'),
    dash.Input({'type': 'gantt-chart', 'index': dash.MATCH}, 'clickData')
)
def display_click_data(clickData):
    if clickData is None:
        return "Click on a bar to view the information."

    point = clickData['points'][0]
    task, place, start, end, description, image = point['customdata']

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.Img(src=image, style={'width': '150px'})
                ]),
                width=2,
                xs=12, md=2
            ),
            dbc.Col(
                html.Div([
                    html.H3(f"{place}"),
                    html.P(f"{task}"),
                    html.P(f"Start date: {start}"),
                    html.P(f"End Date: {end}") if "Digitas" not in place else html.P(f"End Date: Present"),
                ]),
                width=8,
                xs=12, md=10
            ),
        ]),
        html.P(f"\n\n"),
        dcc.Markdown(children=description)
    ])

@dash.callback(
    dash.Output('tabs-content', 'children'),
    dash.Input('tabs', 'value'),
)
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            dbc.Col(
                html.Img(src="assets/images/me/me.jpg", style={'width': '100%', 'height': 'auto', 'display': 'block'}),
                className=f'float-end ms-3 col-4'
            ),
            html.Div(dcc.Markdown(children=ABOUT_ME)),
            html.Div(style={'clear': 'both'})
        ], className='clearfix p-3 border')
    elif tab == 'tab-2':
        return html.Div([
            html.H3("👨‍🎓 Education History"),
            html.P("A tour of my academic journey. This interactive timeline summarizes the institutions and programs that have shaped my knowledge, showcasing my key achievements and academic growth over time."),
            gantt_layout('eductation-chart', MY_DATA['fig_edu'], 'eductation-output-text')
        ])
    elif tab == 'tab-3':
        return html.Div([
            html.H3("👨‍💻 My Professional Journey"),
            html.P("A tour of my professional history. This interactive timeline summarizes the companies and roles that have defined my career, showcasing my progress and contributions over time."),
            gantt_layout('work-chart', MY_DATA['fig_work'], 'work-output-text')
        ])
    elif tab == 'tab-4':
        return skill_section(MY_DATA)
    elif tab == 'tab-6':
        return html.Div([
            html.H3("🎸 Outside of Work"),
            dcc.Markdown(children=MY_HOBBIES),
            dbc.Carousel(
                items=[
                    {"key": "1", "src": "assets/images/me/chichen.jpg", "img_style": IMAGE_STYLE, "caption": "Chichén Itzá"},
                    {"key": "2", "src": "assets/images/me/batman.jpg", "img_style": IMAGE_STYLE, "caption": "Mole Con 2025"},
                    {"key": "3", "src": "assets/images/me/kemonito.jpg", "img_style": IMAGE_STYLE, "caption": "Kemonito M&G"},
                    {"key": "4", "src": "assets/images/me/epica.jpg", "img_style": IMAGE_STYLE, "caption": "Epica M&G"},
                    {"key": "5", "src": "assets/images/me/lego.jpg", "img_style": IMAGE_STYLE, "caption": "Lego collection peek"},
                    {"key": "6", "src": "assets/images/me/festival.jpg", "img_style": IMAGE_STYLE, "caption": "Hell & Heaven 2023 Festival"},
                ],
                controls=True,
                indicators=True,
                style={'background-color': '#CED4DA'}
            )
        ])
