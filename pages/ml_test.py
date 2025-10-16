import dash
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc
from utils.constants import DESCRIPTION_SVM, MY_DATA, MODEL, MLB

dash.register_page(__name__, path='/ml_test', name='ML Test')

layout = html.Div([
    html.H1('Aztec and Mayan Deity Recommender'),
    html.P("This project features a predictive model that recommends an Aztec or Mayan deity to a user based on their musical and film preferences. The solution leverages a Support Vector Machine (SVM) classifier, a powerful supervised learning algorithm, to map user tastes to a specific deity."),
    dcc.Markdown(children=DESCRIPTION_SVM),
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

    html.Button('Send', id='send-button', n_clicks=0),

    html.Div(id='output-prediction', style={'marginTop': '20px', 'fontSize': '18px'})
])

@dash.callback(
    [dash.Output('dropdown-music', 'options'),
    dash.Output('dropdown-films', 'options')],
    dash.Input('shared-data-store', 'data')
)
def actualizar_opciones_ambos_dropdowns(json_data):
    music_options = [{'label': gender.capitalize(), 'value': gender} for gender in MY_DATA['music_subgenres']]
    film_options = [{'label': film.capitalize(), 'value': film} for film in MY_DATA['film_subgenres']]

    return music_options, film_options

@dash.callback(
    dash.Output('output-prediction', 'children'),
    dash.Input('send-button', 'n_clicks'),
    dash.State('dropdown-music', 'value'),
    dash.State('dropdown-films', 'value')
)
def svm_prediction(n_clicks, selected_music, selected_films):
    if n_clicks > 0:
        if selected_music and selected_films:
            user_input = [g.strip() + ' (music)' for g in selected_music] + \
                      [g.strip() + ' (film)' for g in selected_films]
            X_user = MLB.transform([user_input])
            # predictions = model.predict(X_user)
            scores = MODEL.named_steps['svm'].decision_function(MODEL.named_steps['scaler'].transform(X_user))[0]
            top_god = np.argsort(scores)[::-1][:1]
            result = MODEL.named_steps['svm'].classes_[top_god]

            description = MY_DATA['df_gods'][result[0]][0]
            image =MY_DATA['df_gods'][result[0]][1]
            personality = MY_DATA['df_gods'][result[0]][2]

            return html.Div([
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.Img(src=image, style={'width': '500px'})
                        ]),
                    ),
                    dbc.Col(
                        html.Div([
                            html.H1(f"{result[0]}"),
                            html.P(f"{personality}"),
                            html.P(f"{description}"),
                        ]),
                    ),
                ]),
            ])

        else:
            return 'Please select at least one of each genres'
    return ''
