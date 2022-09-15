import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
from dash_table import DataTable, FormatTemplate
import plotly.express as px
import pandas as pd
import numpy as np
from dash import Dash, dash_table
from app import app
import mysql.connector as connection


df = pd.read_csv("assets/processed_data/output.csv")
dat_columns = df.columns


col = ['year','country', 'sex','continent' , 'age', 'sucid_in_hundredk','suicides']

layout = html.Div([
            dbc.Col(children=[
                html.H1('Data Quick View',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    },
                className='text-center pb-3'
                ),

            ]),
        dbc.Row(children=[
            dbc.Col(children=[
                dash_table.DataTable(
                df.to_dict('records'),
                [{"name": i, "id": i} for i in col],
                cell_selectable=False,
                # Add sorting
                sort_action='native',
                # Add filtering
                filter_action='native',
                page_action='native',
                # Start on the first page
                page_current=0,
                # Render 7 items per page
                page_size=30,
                ),
    
        ],style={
                    'textAlign': 'center',
                    'color': '#131414',
                },className='text-center pb-3'),
    ],className="pt-2"        ,style={
            'marginLeft' : '10px',
            'marginRight': '10px',
        }),
            ################### start of footer row #######################   
            
            dbc.Row([
                dbc.Col(children=[
                        dbc.Col(html.H5(children='Copyright © 2022, Dundalk Institute of Technology. All Rights Reserved',
                        className="text-center pt-2 pb-2"),
                                            
                ),
                dbc.Col(children=[
                        dbc.Col(
                        html.H5(children='Mob : +353 89 273 8178',
                        className="text-center pb-2"),
                                    
                    )

                ]),
                dbc.Col(children=[
                        dbc.Col(
                        html.H5(children='Email : d00242726@student.dkit.ie',
                        className="text-center pb-2"),
                                    
                    )

                ])

        ]),
        ],className="pt-2"
        ,style={
            'marginLeft' : '10px',
            'marginRight': '10px',
        }
        )
        ########################### End of Footer #########################
])