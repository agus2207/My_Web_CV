import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.constants import description_svm

dash.register_page(__name__, path='/ml_test', name='ML Test')

layout = html.Div([
    html.H1('Aztec and Mayan Deity Recommender'),
    html.P("This project features a predictive model that recommends an Aztec or Mayan deity to a user based on their musical and film preferences. The solution leverages a Support Vector Machine (SVM) classifier, a powerful supervised learning algorithm, to map user tastes to a specific deity."),
    dcc.Markdown(children=description_svm),
    html.Div([
        html.Img(src='assets/images/gods/Itzpapalotl.png', style={'width': '150px', 'marginRight': '50px'}),
        html.P("I got Itzpapalotl! What about you? Try it yourself. 😎🤟", style={'fontWeight': 'bold', 'flex': 1, 'marginRight': '20px'}),
    ], style={'display': 'flex', 'alignItems': 'center'}),
    html.P('\n\n'),
    html.Div([
        html.P('Music Genres:'),
        dcc.Dropdown(
            id='dropdown-music',
            options=[],
            value=[],
            placeholder="Select at least one music genre",
            multi=True
        ),
        html.P('\n\n'),
        html.P('Film Genres:'),
        dcc.Dropdown(
            id='dropdown-films',
            options=[],
            value=[],
            placeholder="Select at least one film genre",
            multi=True
        ),
    ], style={'width': '50%', 'marginBottom': '20px'}),

    html.Button('Send', id='boton-enviar', n_clicks=0),

    html.Div(id='output-resultado', style={'marginTop': '20px', 'fontSize': '18px'})
])
