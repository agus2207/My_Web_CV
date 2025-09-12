import dash
from dash import html, dcc
import dash_bootstrap_components as dbc # 👈 Importar DBC

# Usar el tema de Bootstrap al inicializar la app
# Puedes cambiar el tema, por ejemplo, dbc.themes.CYBORG para un look oscuro
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Usar un tema de Bootstrap para el estilo
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX])

# Estilos para el sidebar
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# Estilos para el contenido principal
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

# Definir el sidebar
sidebar = html.Div(
    [
        html.H2("Menú", className="display-4"),
        html.Img(src='assets/input_files/images/school/ipn.png', style={'width': '150px'}),
        html.Hr(),
        html.P("Navegación", className="lead"),
        dbc.Nav(
            [
                # Usamos dbc.NavLink para los enlaces
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
    style=SIDEBAR_STYLE,
)

# Definir el layout de la app con el sidebar y el contenido
app.layout = html.Div(
    [
        dcc.Location(id="url"), # Necesario para la navegación en el sidebar
        sidebar,
        html.Div(id="page-content", children=dash.page_container, style=CONTENT_STYLE),
    ]
)

if __name__ == "__main__":
    app.run(debug=True)
