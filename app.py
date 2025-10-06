import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import os
import joblib
from utils.callbacks import register_all_callbacks
from utils.constants import SIDEBAR_STYLE, CONTENT_STYLE

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.LUX, dbc.icons.BOOTSTRAP], suppress_callback_exceptions=True)

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
    ]
)

model = joblib.load('assets/datasets/svm_model_gods.pkl')
mlb = joblib.load('assets/datasets/mlb_gods.pkl')
register_all_callbacks(app, model, mlb)

if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
