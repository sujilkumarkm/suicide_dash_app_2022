
# import dash
from turtle import color
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
# df = df.iloc[10:1000]
columnss=list(df.columns)
country_names = df['country'].unique()

cont_names = df['continent'].unique()


from app import app

color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


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
                                value=country_names,
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
                                    max=1000,
                                    value=[0,100],
                                    step= 1,
                                    marks={
                                        0: '1',
                                        200: '200',
                                        400: '400',
                                        800: '800+',
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
                html.Label('Select Variable to display on the Graphs'),
                dcc.Dropdown(id='y_dropdown',
                    options=[
                        {'label': 'Suicide', 'value': 'suicides'},
                        {'label': 'Population', 'value': 'population'},
                        {'label': 'GDP', 'value': 'gdp_per_capita'}],
                    value='population'
                )]),
            dbc.Row([
                 dbc.Col(html.Div(children=[
                dcc.Graph(id="LifeExps")],className='mt-3 ml-3')
                ,className='col-6 col-sm-6 col-md-6'),
                dbc.Col(html.Div(children=[
                    dcc.Graph(id="LifeExpOverTimes")],style={}, className='mt-3 mr-3')
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

# @app.callback(
#     [Output(component_id='distance_graph', component_property='figure'),
#      Output(component_id='count_dist_graph', component_property='figure'),
#      Output(component_id='shot_graph', component_property='figure'),
#      Output(component_id='scat_graph', component_property='figure'),],
#     [Input(component_id='country_drop', component_property='value'),
#      Input(component_id='suicides_slider', component_property='value'),
#      Input(component_id='y_dropdown', component_property='value'),
#     ]
# )
# def update_line_chart(country_names, range_chosen, eur_yxx_dropdown):
#     if not (country_names or range_chosen or eur_yxx_dropdown):
#         return dash.no_update
#     d = df[(df['suicides'] >= range_chosen[0]) & (df['suicides'] <= range_chosen[1])]
#     data =[]
#     for j in country_names:
#             data.append(d[d['country'] == j])
#     dff = pd.DataFrame(np.concatenate(data), columns=columnss)
#     dff=dff.infer_objects()
#     mask = dff.country.isin(country_names)
#     # fig = px.scatter(dff[mask], 
#     # x="population", y="suicides", color="country", size='population',
#     #              hover_name="sex", size_max=60)
#     fig= px.choropleth(dff[mask],               
#               locations="country_code", 
#               color="suicides",
#               hover_name="country",  
#               animation_frame="year",
#               title="World map of Suicides")
#     fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
#         plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
#         showlegend=False)

#     mask2 = dff.country.isin(country_names)
#     fig2 = px.histogram(dff[mask2],x="sex", y="population", color='country')

#     mask1 = dff.country.isin(country_names)
#     # fig1 = px.bar(dff[mask1],x="country", y="population", color='population')
#     fig1 = px.sunburst(dff[mask1], path=['sex', 'country', 'country_code'], values='suicides')

#     mask3 = dff.country.isin(country_names)
#     fig3 = px.scatter(dff[mask3],x="sucid_in_hundredk", y="population", color='sex')
    
#     return fig, fig1, fig2, fig3




@app.callback(
    [Output(component_id='LifeExps', component_property='figure'),
    Output(component_id='LifeExpOverTimes', component_property='figure')],
    [Input(component_id='country_drop', component_property='value'),
     Input(component_id='suicides_slider', component_property='value'),
     Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,slider_val,yvar):
    if not (selected_cont or slider_val or yvar):
        return dash.no_update
    d = df[(df['suicides'] >= slider_val[0]) & (df['suicides'] <= slider_val[1])]
    data =[]
    for j in selected_cont:
            data.append(d[d['continent'] == j])
    dff = pd.DataFrame(np.concatenate(data), columns=columnss)
    dff=dff.infer_objects()
    map_fig= px.choropleth(dff,locations="country", color=dff[yvar],
            hover_name="country",hover_data=['continent','population'],animation_frame="year",    
            color_continuous_scale='Turbo',range_color=[dff[yvar].min(), dff[yvar].max()],
            labels={'population':'Population','year':'Year','continent':'Continent',
                'country':'Country','suicides':'Suicide'})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=dff, 
                x="year",  y = dff[yvar] , color='continent',line_group="country", 
                hover_data=['population','year'],
                 # Add bold variable in hover information
                hover_name='country',color_discrete_map=color_discrete_map,
                 # change labels
                labels={'population':'Population','year':'Year','continent':'Continent',
                     'country':'Country','suicides':'Total Suicides'})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]

