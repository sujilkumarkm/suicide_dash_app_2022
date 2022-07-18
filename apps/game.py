import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from gapminder import gapminder

import plotly.express as px
import pandas as pd
import numpy as np

#data for the gaelic plots
loc_data = pd.read_csv('assets/cleaned_data.csv')



# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#e9eef5',
    'text': '#1c1cbd'
}
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div([
################### start of first row #######################   
   
        dbc.Row(children=[
            dbc.Col(children=[
                html.H1('Overlooking Gaelic',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    },
                className='text-center'
                ),

            ]),
        ]),
        dbc.Row(children=[
            dbc.Col(children=[
                html.Label('Select Variable to display on Graph'),
                dcc.Dropdown(id='y_dropdown',
                options=[
                            {'label': 'Distance from Goal', 'value': 'distance_from_goal'},
                            {'label': 'Short Pressure', 'value': 'shot_pressure'},
                            {'label': 'Shot Type', 'value': 'shot_type'},
                            {'label': 'Set Play', 'value': 'set_play'},
                            {'label': 'Shot Method', 'value': 'shot_method'},
                            {'label': 'Shot Outcome', 'value': 'shot_outcome'},
                            {'label': 'Assist Type', 'value': 'assist_type'}],
                value='shot_pressure',
                style = {
                            # 'textAlign': 'center',
                            'color': '#1c1818',
                            'width' : '50%'
                        },
            ),
            ],className='ml-3 mb-3'),
        ]),
        dcc.Graph(
            id='line_graph',
            style={
            'textAlign': 'center',
            'color': colors['text'],
            'margin': '15px'},
        ),
        dcc.Graph(
        id='line_graph1',
        style={
        'textAlign': 'center',
        'color': colors['text'],
        'margin': '15px'},
        ),
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
    ],className="pt-2"),
])

@app.callback(
    [Output(component_id='line_graph', component_property='figure'),
     Output(component_id='line_graph1', component_property='figure')],
    [Input(component_id='y_dropdown', component_property='value')]
)
def update_map(yvar):
    df = loc_data
    line_fig = px.line(data_frame=df, 
                x="shot_id",  y = df[yvar] , color='county',line_group="county", 
                hover_data=['assist_type','county'],
                 # Add bold variable in hover information
                  hover_name='shot_id',
                 # change labels
                 labels={'Game':'game','Shot Type':'shot_type','Counties':'county',
                     'Assist Type':'assist_type','Shot Method':'shot_method', 'Set Play':'set_play', 'Distance from Goal':'distance_from_goal'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
    
    line_fig1 = fig = px.histogram(df, x="shot_outcome", color=df[yvar])
    line_fig1.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [line_fig, line_fig1]