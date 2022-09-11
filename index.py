from dash import dcc
from dash import html
from app import server
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

# must add this line in order for the app to be deployed successfully on Heroku
# from app import server
from app import app
from app import server
# import all pages in the app
from apps import dashboard, forecast1, overview, policy, home, data, outliers, about, general, generations

# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Dashboard", href="/dashboard"),
        dbc.DropdownMenuItem("Overview", href="/overview"),
        dbc.DropdownMenuItem("Generations", href="/generations"),
        # dbc.DropdownMenuItem("General", href="/general"),
        dbc.DropdownMenuItem("Forecast Models", href="/forecast1"),
        dbc.DropdownMenuItem("Data Integrity", href="/outliers"),
        dbc.DropdownMenuItem("Data View", href="/data"),
        dbc.DropdownMenuItem("Feedback", href="https://www.dkit.ie.narayam.net/contact",target="_blank",),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore Pages",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/dkit_logo.png", height="60px")),
                        dbc.Col(dbc.NavbarBrand("Suicide Analysis Dashboard", className="")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="nav-link dropdown-toggle"
                ),
                navbar=True,
            ),
            html.A(dbc.Row(
                    [                        
                        dbc.DropdownMenuItem("About Us", className="ml-2"),
                    ],
                    align="center",
                ),href="/about",),
        ]
    ),sticky="top",
    color="dark",
    dark=True,  
    className="mb-4",
)
row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div("A single column"))),
        dbc.Row(
            [
                dbc.Col(html.Div("One of three columns")),
            ]
        ),
    ]
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# embedding the navigation bar
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/policy':
        return policy.layout
    elif pathname == '/dashboard':
        return dashboard.layout
    elif pathname == '/overview':
        return overview.layout
    elif pathname == '/forecast1':
        return forecast1.layout
    elif pathname == '/outliers':
        return outliers.layout
    elif pathname == '/data':
        return data.layout
    elif pathname == '/about':
        return about.layout
    elif pathname == '/general':
        return general.layout
    elif pathname == '/generations':
        return generations.layout
    
    else:
        return home.layout


if __name__ != '__main__':
    pass
else:
    app.run_server(port=8000, debug=True, host='0.0.0.0')