from dash import dcc, html, Input, Output, MATCH, State
import dash_bootstrap_components as dbc
import dash
import json
import numpy as np
import pandas as pd
from datetime import datetime
from utils.create_layouts import *
from utils.constants import SIDEBAR_STYLE, CONTENT_STYLE, CONTENT_STYLE_HIDDEN

model = None
mlb = None

def register_all_callbacks(app, model_load, mlb_load):

    global model
    global mlb
    model, mlb = model_load, mlb_load

    @app.callback(
        [
            dash.Output('sidebar', 'style'),
            dash.Output('page-content', 'style'),
            dash.Output('toggle-button', 'children')
        ],
        [dash.Input('toggle-button', 'n_clicks')]
    )
    def toggle_sidebar(n_clicks):
        if n_clicks % 2 == 0:
            return SIDEBAR_STYLE, CONTENT_STYLE, html.I(className="bi bi-arrow-left-square")
        else:
            return {'display': 'none'}, CONTENT_STYLE_HIDDEN, html.I(className="bi bi-arrow-right-square")

    @app.callback(
        dash.Output('shared-data-store', 'data'),
        dash.Input('shared-data-store', 'data')
    )
    def cargar_y_guardar_dataframes(data):
        if data is None:
            today = datetime.now()
            today_str = today.strftime('%Y-%m-%d')
            df_me = pd.read_csv("assets/datasets/experience.csv", encoding="latin-1", low_memory=False)
            df_me['Finish'] = np.where(df_me['Place'].str.contains('Digitas', case=False, na=False), today_str, df_me['Finish'])
            df_me['Start_str'] = pd.to_datetime(df_me['Start'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
            df_me['Finish_str'] = pd.to_datetime(df_me['Finish'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')
            df_skills = pd.read_csv("assets/datasets/skills.csv", encoding="latin-1", low_memory=False)
            df_gods = pd.read_csv("assets/datasets/gods.csv", encoding="latin-1", low_memory=False)
            df_gods['music subgenres'] = df_gods['music subgenres'].str.split(', ')
            df_gods['film subgenres'] = df_gods['film subgenres'].str.split(', ')
            music_subgenres = [item for sublist in df_gods['music subgenres'] for item in sublist]
            music_subgenres = list(set(music_subgenres))
            film_subgenres = [item for sublist in df_gods['film subgenres'] for item in sublist]
            film_subgenres = list(set(film_subgenres))

            data_to_store = {
                'df_gods': df_gods[['god', 'descriptive text', 'Image URL', 'personality']].to_json(orient='split'),
                'music_subgenres':music_subgenres,
                'film_subgenres':film_subgenres,
                'fig_edu':create_timeline(df_me[df_me['Type'] == 'School']).to_json(),
                'fig_work':create_timeline(df_me[df_me['Type'] == 'Work']).to_json(),
                'fig_pl':create_radar(df_skills[df_skills['Type'] == 'Programming Languages'], 'Programming Languages Domain').to_json(),
                'fig_bi':create_bar(df_skills[df_skills['Type'] == 'BI'], 'BI Domain').to_json(),
                'fig_li':create_map(df_skills[df_skills['Type'] == 'Libraries'], 'Python Libraries Domain', 'Python Libraries').to_json(),
                'fig_apache':create_pie(df_skills[df_skills['Type'] == 'Apache'], 'Apache Knowleadge').to_json(),
                'fig_sql':create_radar(df_skills[df_skills['Type'] == 'DBMS'], 'DBMS Domain').to_json(),
                'fig_cloud':create_map(df_skills[df_skills['Type'] == 'Cloud'], 'Cloud Computing Domain', 'Cloud Computing').to_json(),
                'fig_learning':create_pie(df_skills[df_skills['Type'] == 'Learning'], 'Tech Learning').to_json(),
                'fig_tech':create_bar(df_skills[df_skills['Type'] == 'Tech'], 'Tech Knowleadge').to_json(),
                'fig_agile':create_pie(df_skills[df_skills['Type'] == 'Agile'], 'Known Agile Methodologies').to_json(),
                'fig_lan':create_bar(df_skills[df_skills['Type'] == 'Languages'], 'Spoken Languages').to_json(),
                'fig_marketing':create_pie(df_skills[df_skills['Type'] == 'Marketing'], 'Marketing').to_json(),
            }

            del df_skills
            del df_me
            del df_gods
            return json.dumps(data_to_store)
        return dash.no_update

    @app.callback(
        Output({'type': 'gantt-output-text', 'index': MATCH}, 'children'),
        Input({'type': 'gantt-chart', 'index': MATCH}, 'clickData')
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

    @app.callback(
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
                gantt_layout('eductation-chart', json.loads(data_dict['fig_edu']), 'eductation-output-text')
            ])
        elif tab == 'tab-3':
            return html.Div([
                html.H3("My Professional Journey"),
                html.P("A tour of my professional history. This interactive timeline summarizes the companies and roles that have defined my career, showcasing my progress and contributions over time."),
                gantt_layout('work-chart', json.loads(data_dict['fig_work']), 'work-output-text')
            ])
        elif tab == 'tab-4':
            return skill_section(data_dict)

    @app.callback(
        [Output('dropdown-music', 'options'),
         Output('dropdown-films', 'options')],
        Input('shared-data-store', 'data')
    )
    def actualizar_opciones_ambos_dropdowns(json_data):
        if json_data is None:
            return [], []

        data_dict = json.loads(json_data)
        music = data_dict['music_subgenres']
        films = data_dict['film_subgenres']
        music_options = [{'label': gender.capitalize(), 'value': gender} for gender in music]
        film_options = [{'label': film.capitalize(), 'value': film} for film in films]

        return music_options, film_options

    @app.callback(
        Output('output-resultado', 'children'),
        Input('boton-enviar', 'n_clicks'),
        Input('shared-data-store', 'data'),
        State('dropdown-music', 'value'),
        State('dropdown-films', 'value')
    )
    def ejecutar_funcion(n_clicks, json_data, selected_music, selected_films):
        if n_clicks > 0:
            if selected_music and selected_films:
                gustos_combinados = [g.strip() + ' (music)' for g in selected_music] + \
                       [g.strip() + ' (film)' for g in selected_films]
                X_usuario = mlb.transform([gustos_combinados])
                prediccion = model.predict(X_usuario)
                scores = model.named_steps['svm'].decision_function(model.named_steps['scaler'].transform(X_usuario))[0]
                top_indices = np.argsort(scores)[::-1][:1]
                deidades_posibles = model.named_steps['svm'].classes_[top_indices]

                data_dict = json.loads(json_data)
                gods = json.loads(data_dict['df_gods'])
                lookup_dict = {item[0]: {'Description': item[1], 'Image': item[2], 'Personality': item[3]} for item in gods['data']}
                description = lookup_dict[deidades_posibles[0]]['Description']
                image = lookup_dict[deidades_posibles[0]]['Image']
                personality = lookup_dict[deidades_posibles[0]]['Personality']

                return html.Div([
                    dbc.Row([
                        dbc.Col(
                            html.Div([
                                html.Img(src=image, style={'width': '500px'})
                            ]),
                        ),
                        dbc.Col(
                            html.Div([
                                html.H1(f"{deidades_posibles[0]}"),
                                html.P(f"{personality}"),
                                html.P(f"{description}"),
                            ]),
                        ),
                    ]),
                ])

            else:
                return 'Please select at least one of each genres'
        return ''
