import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from flask_compress import Compress
# import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from utils.constants import SIDEBAR_STYLE, CONTENT_STYLE, CONTENT_STYLE_HIDDEN, WHATSAPP_ICON, EMAIL_ICON, LINKEDIN_ICON, GITHUB_ICON

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True, prevent_initial_callbacks=True, update_title=None,
    serve_locally=True)

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

server = app.server
Compress(server)

limiter = Limiter(
    get_remote_address,
    # server,
    app=server,
    storage_uri="memory://",
    default_limits=["5/second"],
)

@limiter.request_filter
def header_whitelist():
    # Si la ruta contiene '_dash' o 'assets', no aplicar límite
    from flask import request
    return any(x in request.path for x in ["_dash-", "assets", "static"])

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
        html.Div(
            [
                html.Div([GITHUB_ICON, LINKEDIN_ICON, WHATSAPP_ICON, EMAIL_ICON], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'marginBottom': '10px'}),
                html.P("📫agusgalrey22@proton.me", style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'marginBottom': '10px'}),
                # html.P("📞+52 56 5356 0123", style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'marginBottom': '10px'}),
                html.Button("Download my CV", id="btn-download-csv", style={'width': '100%'}),
                dcc.Download(id="download-csv")
            ],
            style={'marginTop': 'auto', 'paddingTop': '1rem'}
        )
    ],
    id="sidebar",
    style=SIDEBAR_STYLE,
)

toggle_button = dbc.Button(
    html.I(className="bi bi-arrow-left-square"),
    id="toggle-button",
    n_clicks=0,
    style={
        "position": "fixed",
        "top": "0rem",
        "left": "0rem",
        "background-color": "transparent",
        "border": "none",
        "font-size": "1.5rem",
        "z-index": "100",
        "color": "black",
        "transition": "all 0.3s"
    }
)

app.layout = html.Div(
    [
        dcc.Location(id="url"),
        dcc.Store(id='shared-data-store'),
        sidebar,
        toggle_button,
        html.Div(id="page-content", children=dash.page_container, style=CONTENT_STYLE),
    ],
    style={"background-color": "#E9ECEF"}
)

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
    dash.Output("download-csv", "data"),
    dash.Input("btn-download-csv", "n_clicks"),
    prevent_initial_call=True,
)
def download_file(n_clicks):
    return dcc.send_file("assets/CVAgustinGalindoReyes.pdf")

# if __name__ == "__main__":
#     app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
