import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path='/contact', name='Contact me')

layout = dbc.Container(
    html.Div(
        children=[
            html.H2("Contacto", className="display-4 text-success"),
            html.P("Puedes contactarme a través de este formulario o mis redes sociales.", className="lead"),
            dbc.Row( # 👈 Usar dbc.Row y dbc.Col para el diseño de columnas
                [
                    dbc.Col(html.A("LinkedIn", href="#", className="btn btn-dark"), width=6, className="text-center"),
                    dbc.Col(html.A("GitHub", href="#", className="btn btn-dark"), width=6, className="text-center"),
                ],
                className="mt-4"
            )
        ],
        className="p-5 my-5 bg-dark text-white rounded-3"
    )
)
