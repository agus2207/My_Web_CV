import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from datetime import datetime

class GanttComponent:
    def __init__(self, app, df: pd.DataFrame, id_prefix: str):
        self.app = app
        self.df = df
        self.id_prefix = id_prefix

        self.graph_id = f'{self.id_prefix}-chart'
        self.output_id = f'{self.id_prefix}-output-text'

        self.register_callbacks()

    def get_layout(self):
        fig = px.timeline(
            self.df,
            x_start="Start",
            x_end="Finish",
            y="Place",
            color="Place",
            custom_data=["Item", "Place", "Start_str", "Finish_str", "Description", "Imagen"]
        )
        fig.update_yaxes(autorange="reversed")

        return html.Div([
            dcc.Graph(id=self.graph_id, figure=fig),
            html.Div(
                id=self.output_id,
                style={'margin-top': '20px', 'font-size': '18px'}
            )
        ])

    def register_callbacks(self):
        @self.app.callback(
            Output(self.output_id, 'children'),
            Input(self.graph_id, 'clickData')
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
