
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go

#data for the gaelic plots
df = pd.read_csv('assets/cleaned_data.csv')
columnss=list(df.columns)
county_names = df['county'].unique()


from app import app

color_discrete_map = {'Cavan': '#636EFA', 'Armagh': '#EF553B', 'Down': '#00CC96',
    'Dublin': '#AB63FA', 'Kerry': '#FFA15A'}


layout = html.Div([
################### start of first row #######################   
                html.H1('Gaelic Shot Statistics',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                    dbc.Col(children=[
                    html.Label('Select Counties'),
                    dcc.Dropdown(id='county_drop',
                                options=[{'label': i, 'value': i}
                                        for i in county_names],
                                value=['Cavan', 'Armagh', 'Down', 'Dublin', 'Kerry'],
                                multi=True,
                                style={
                                    # 'textAlign': 'center',
                                    'color': '#1c1818',
                                }
                    )
                    ], className='ml-2 mb-2'),  
                        dbc.Col(html.Div([
                                dbc.Col(children=[
                                html.Label('Select Build Up Pass Range'),
                                dcc.RangeSlider(id='pass_range',
                                    min=0,
                                    max=29,
                                    value=[0,29],
                                    step= 1,
                                    marks={
                                        0: '0',
                                        10: '10',
                                        20: '20',
                                        29: '29',
                                    },
                                )
                                ]),
                                ],className='pb-2')
                        ),
                        # dcc.Dropdown(id='var_drop',
                        # options=[                    
                        #     {'label': 'game', 'value': 'game'},
                        #     {'label': 'shot_method', 'value': 'shot_method'},
                        #     {'label': 'set_play', 'value': 'set_play'},
                        #     ],
                        # value='game',
                        # style={
                        #             # 'textAlign': 'center',
                        #             'color': '#1c1818',
                        #       },
                        # )
                        #              ],className='pb-2')]
                        # )),
                    ]),

################### End of first row #######################   
            dbc.Row([
                dbc.Col(html.Div(children=[
                    dcc.Graph(id="distance_graph")],className='ml-3 mt-3')
                    ,className='col-6 col-sm-6 col-md-6'),
                dbc.Col(html.Div(children=[
               
                    dcc.Graph(id="scat_graph")],className='mr-3 mt-3')
                    ,className='col-6 col-sm-6 col-md-6'),

            ], 
            className='text-center pt-2 pb-2',
            style={}),

################### End of second row #######################    

            dbc.Row([
                 dbc.Col(html.Div(children=[
                dcc.Graph(id="count_dist_graph")],className='mt-3 ml-3')
                ,className='col-6 col-sm-6 col-md-6'),
                dbc.Col(html.Div(children=[
                    dcc.Graph(id="shot_graph")],style={}, className='mt-3 mr-3')
                    ,className='col-6 col-sm-6 col-md-6'),
            ], 
            className='text-center pt-2 pb-2',
            style={}),

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
    ],className="pt-2")

])


@app.callback(
    [Output(component_id='distance_graph', component_property='figure'),
     Output(component_id='shot_graph', component_property='figure'),
     Output(component_id='scat_graph', component_property='figure'),
     Output(component_id='count_dist_graph', component_property='figure')],
    [Input(component_id='county_drop', component_property='value'),
     Input(component_id='pass_range', component_property='value'),
    ]
)
def update_line_chart(county_names, range_chosen):
    d = df[(df['build_up_passes'] >= range_chosen[0]) & (df['build_up_passes'] <= range_chosen[1])]
    data =[]
    for j in county_names:
            data.append(d[d['county'] == j])
    dff = pd.DataFrame(np.concatenate(data), columns=columnss)
    dff=dff.infer_objects()
    mask = dff.county.isin(county_names)
    fig = px.scatter(dff[mask], 
    x="distance_from_goal", y="build_up_passes", color="county", size='distance_from_goal',
                 hover_name="shot_outcome", size_max=60)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False)
    mask2 = dff.county.isin(county_names)
    fig2 = px.histogram(dff[mask2],x="shot_outcome", y="distance_from_goal", color='county')

    mask1 = dff.county.isin(county_names)
    # fig1 = px.bar(dff[mask1],x="county", y="distance_from_goal", color='distance_from_goal')
    fig1 = px.sunburst(dff[mask1], path=['shot_outcome', 'county', 'assist_type'], values='build_up_passes')

    mask3 = dff.county.isin(county_names)
    fig3 = px.scatter(dff[mask3],x="angle", y="distance_from_goal", color='shot_outcome')
    
    return fig, fig1, fig2, fig3





