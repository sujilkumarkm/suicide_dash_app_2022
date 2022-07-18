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
from apps import dashboard, game, policy, home, data

# building the navigation bar
dropdown = dbc.DropdownMenu(
    children=[
        # dcc.Link("Game", href="/apps/game"),
        dbc.DropdownMenuItem("Dashboard", href="/dashboard"),
        # dbc.DropdownMenuItem("Policy", href="/policy"),
        dbc.DropdownMenuItem("Overview", href="/game"),
        dbc.DropdownMenuItem("Data View", href="/data"),
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
                        dbc.Col(dbc.NavbarBrand("Gaelic Analysis Dashboard", className="ml-2")),
                    ],
                    align="center",
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    # right align dropdown menu with ml-auto className
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
            html.A(dbc.Row(
                    [                        
                        dbc.DropdownMenuItem("About Us", className="ml-2"),
                    ],
                    align="center",
                ),href="/home#aboutme",),
                 html.A(dbc.Row(
                    [                        
                        dbc.DropdownMenuItem("Privacy Policy", className="ml-2"),
                    ],
                    align="center",
                ),href="/policy",),
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
    # elif pathname == '/Europe':
    #     return Europe.layout
    elif pathname == '/game':
        return game.layout
    elif pathname == '/data':
        return data.layout
    
    else:
        return home.layout


if __name__ != '__main__':
    pass
else:
    app.run_server(port=8000, debug=False)