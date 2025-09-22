import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

CONTENT_STYLE_HIDDEN = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "transition": "all 0.3s"
}

sidebar = html.Div(
    [
        # html.Img(src='assets/input_files/images/school/ipn.png', style={'width': '150px'}),
        html.Hr(),
        html.P("Navigation", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink(
                    f"{page['name']}",
                    href=page["path"],
                    active="exact"
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
        ),
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

toggle_button = dbc.Button(
    html.I(className="bi bi-arrow-left-square"), # Ícono de flecha izquierda por defecto
    id="toggle-button",
    n_clicks=0,
    style={
        "position": "fixed",
        "top": "0rem",
        "left": "0rem",
        "background-color": "transparent",
        "border": "none",
        "font-size": "1.5rem",
        "z-index": "100", # Para que esté encima de otros elementos
        "color": "black",
        "transition": "all 0.3s"
    }
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        toggle_button,
        html.Div(id="page-content", children=dash.page_container, style=CONTENT_STYLE),
    ]
)

@app.callback(
    # Múltiples salidas: el estilo de la sidebar, el estilo del contenido y el ícono del botón
    [
        dash.Output('sidebar', 'style'),
        dash.Output('page-content', 'style'),
        dash.Output('toggle-button', 'children')
    ],
    # Entrada: el número de clics en el botón
    [dash.Input('toggle-button', 'n_clicks')]
)
def toggle_sidebar(n_clicks):
    if n_clicks % 2 == 0:
        # Estado inicial (o n_clicks par): mostrar sidebar y flecha izquierda
        return SIDEBAR_STYLE, CONTENT_STYLE, html.I(className="bi bi-arrow-left-square")
    else:
        # n_clicks impar: ocultar sidebar y mostrar flecha derecha
        return {'display': 'none'}, CONTENT_STYLE_HIDDEN, html.I(className="bi bi-arrow-right-square")

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
    # app.run(debug=True)
