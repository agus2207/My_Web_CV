import dash
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.constants import DESCRIPTION_SVM, MY_DATA, MODEL, MLB

dash.register_page(__name__, path='/ml_test', name='ML Test')

layout = html.Div([
    html.H1('Aztec and Mayan Deity Recommender'),
    dcc.Markdown(children=DESCRIPTION_SVM),
    html.Div([
        html.Img(src='assets/images/gods/Tezcatlipoca.png', style={'width': '200px', 'marginRight': '50px'}),
        html.P("I got Tezcatlipoca! What about you? Try it yourself. 😎🤟", style={'fontWeight': 'bold', 'flex': 1, 'marginRight': '20px', 'fontStyle': 'italic'}),
    ], style={'display': 'flex', 'alignItems': 'center'}),
    html.P('\n\n'),
    html.P('Tip: Select more genres! The more you choose, the better and more accurate your prediction will be.', style={'fontStyle': 'italic', 'fontWeight': 'bold'}),
    html.Div([
        html.P('Music Genres:', style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='dropdown-music',
            options=[],
            value=[],
            placeholder="Select at least one music genre",
            multi=True
        ),
        html.P('\n\n'),
        html.P('Film Genres:', style={'fontWeight': 'bold'}),
        dcc.Dropdown(
            id='dropdown-films',
            options=[],
            value=[],
            placeholder="Select at least one film genre",
            multi=True
        ),
    ], style={'width': '50%', 'marginBottom': '20px'}),

    html.Button('Send', id='send-button', n_clicks=0),

    html.Div(id='output-prediction', style={'marginTop': '20px', 'fontSize': '18px'})
])

@dash.callback(
    [dash.Output('dropdown-music', 'options'),
    dash.Output('dropdown-films', 'options')],
    dash.Input('shared-data-store', 'data')
)
def update_dropdowns(json_data):
    music_options = [{'label': gender.capitalize(), 'value': gender} for gender in MY_DATA['music_subgenres']]
    film_options = [{'label': film.capitalize(), 'value': film} for film in MY_DATA['film_subgenres']]

    return music_options, film_options

@dash.callback(
    dash.Output('output-prediction', 'children'),
    dash.Input('send-button', 'n_clicks'),
    dash.State('dropdown-music', 'value'),
    dash.State('dropdown-films', 'value')
)
def rf_prediction(n_clicks, selected_music, selected_films):
    if n_clicks > 0:
        if selected_music and selected_films:
            user_input = [g.strip().lower() + ' (music)' for g in selected_music] + \
                      [g.strip().lower() + ' (film)' for g in selected_films]
            user_vector = MLB.transform([user_input])
            probs = MODEL.predict_proba(user_vector)[0]
            top_idx = np.argsort(probs)[::-1][:3]
            results = [(MODEL.classes_[i], float(probs[i])) for i in top_idx]

            description = MY_DATA['df_gods'][results[0][0]][0]
            image =MY_DATA['df_gods'][results[0][0]][1]
            personality = MY_DATA['df_gods'][results[0][0]][2]


            return html.Div([
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.Img(src=image, style={'width': '500px'})
                        ]),
                    ),
                    dbc.Col(
                        html.Div([
                            html.H1(f"{results[0][0]}"),
                            html.P(f"{personality}"),
                            html.P(f"{description}"),
                            html.H3(f"Your Top 3 Deities:"),
                            html.P(f"{results[0][0]} - {results[0][1]*100:.1f}% match"),
                            html.P(f"{results[1][0]} - {results[1][1]*100:.1f}% match"),
                            html.P(f"{results[2][0]} - {results[2][1]*100:.1f}% match"),
                        ]),
                    ),
                ]),
            ])

        else:
            return 'Please select at least one of each genres'
    return ''
