
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pytz import country_names
import mysql.connector as connection

#data for the Suicide plots
mydb = connection.connect(host="localhost", database = 'dkit',user="root", passwd="",use_pure=True)
query = "Select * from suicides;"
df = pd.read_sql(query,mydb)
df = df.iloc[10:1000]
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app

color_discrete_map = {'Cavan': '#636EFA', 'Armagh': '#EF553B', 'Down': '#00CC96',
    'Dublin': '#AB63FA', 'Kerry': '#FFA15A'}


layout = html.Div([
################### start of first row #######################   
                html.H1('Suicide Statistics Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                    dbc.Col(children=[
                    html.Label('Select Countries'),
                    dcc.Dropdown(id='country_drop',
                                options=[{'label': i, 'value': i}
                                        for i in country_names],
                                value=['Argentina', 'Armenia', 'Australia', 'Austria', 'Belgium',
                                        'Brazil', 'Bulgaria', 'Canada', 'Chile', 'Colombia', 'Croatia',
                                        'Cuba', 'Czech Republic', 'Denmark', 'Finland', 'France',
                                        'Germany', 'Greece', 'Hungary', 'Iceland', 'Ireland', 'Israel',
                                        'Italy', 'Japan', 'Mexico', 'Netherlands', 'New Zealand', 'Norway',
                                        'Poland', 'Portugal', 'Romania', 'Russian Federation',
                                        'South Africa', 'Spain', 'Sweden', 'Switzerland', 'Thailand',
                                        'Turkmenistan', 'Ukraine'],
                                multi=True,
                                style={
                                    # 'textAlign': 'center',
                                    'color': '#1c1818',
                                }
                    )
                    ], className='ml-2 mb-2'),  
                        dbc.Col(html.Div([
                                dbc.Col(children=[
                                html.Label('Select Suicide Range'),
                                dcc.RangeSlider(id='suicides_slider',
                                    min=0,
                                    max=29,
                                    value=[0,29],
                                    step= 1,
                                    marks={
                                        0: '19',
                                        10: '10',
                                        20: '20',
                                        29: '29',
                                    },
                                )
                                ]),
                                ],className='pb-2')
                        ),
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
    [Input(component_id='country_drop', component_property='value'),
     Input(component_id='suicides_slider', component_property='value'),
    ]
)
def update_line_chart(country_names, range_chosen):
    d = df[(df['suicides'] >= range_chosen[0]) & (df['suicides'] <= range_chosen[1])]
    data =[]
    for j in country_names:
            data.append(d[d['country'] == j])
    dff = pd.DataFrame(np.concatenate(data), columns=columnss)
    dff=dff.infer_objects()
    mask = dff.country.isin(country_names)
    # fig = px.scatter(dff[mask], 
    # x="population", y="suicides", color="country", size='population',
    #              hover_name="sex", size_max=60)
    fig= px.choropleth(dff[mask],               
              locations="country_code", color="gdp_per_capita",
              hover_name="country",  
              animation_frame="year")
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False)
    mask2 = dff.country.isin(country_names)
    fig2 = px.histogram(dff[mask2],x="sex", y="population", color='country')

    mask1 = dff.country.isin(country_names)
    # fig1 = px.bar(dff[mask1],x="country", y="population", color='population')
    fig1 = px.sunburst(dff[mask1], path=['sex', 'country', 'country_code'], values='suicides')

    mask3 = dff.country.isin(country_names)
    fig3 = px.scatter(dff[mask3],x="sucid_in_hundredk", y="population", color='sex')
    
    return fig, fig1, fig2, fig3





