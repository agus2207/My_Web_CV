from dash import dcc, html, Input, Output, MATCH, State
import dash_bootstrap_components as dbc
import dash
import json
import numpy as np
import pandas as pd
from datetime import datetime
from utils.skills import *
from utils.constants import SIDEBAR_STYLE, CONTENT_STYLE, CONTENT_STYLE_HIDDEN

def register_all_callbacks(app):
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
            # Estado inicial (o n_clicks par): mostrar sidebar y flecha izquierda
            return SIDEBAR_STYLE, CONTENT_STYLE, html.I(className="bi bi-arrow-left-square")
        else:
            # n_clicks impar: ocultar sidebar y mostrar flecha derecha
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
            # df_work = df[df['Type'] == 'Work']
            # df_edu = df[df['Type'] == 'School']
            df_skills = pd.read_csv("assets/datasets/skills.csv", encoding="latin-1", low_memory=False)

            # Guarda ambos en un diccionario y lo serializa a JSON
            data_to_store = {
                # 'df_educacion': df_edu.to_json(orient='split'),
                # 'df_trabajo': df_work.to_json(orient='split'),
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
            }

            del df_skills
            del df_me
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
