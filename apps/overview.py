#import packages to create app
from locale import locale_alias
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import mysql.connector as connection
import plotly.express as px
import pandas as pd
import numpy as np
from dash.dash_table import DataTable, FormatTemplate


#data for the Suicide plots
mydb = connection.connect(host="204.93.172.126", database = 'dkitienarayam_db',user="dkitienarayam_admin", passwd="Unnikuttan@1991",use_pure=True)
query = "Select * from suicides;"
loc_data = pd.read_sql(query,mydb)
df = loc_data
loc_cols=list(loc_data.columns)
cols=list(loc_data.columns)
# loc_data = loc_data.iloc[10:1000]
country_names = loc_data['country'].unique()

cont_names = loc_data['continent'].unique()


# needed only if running this as part of a multipage app
from app import app
#app = dash.Dash(__name__)
#change background and color text
colors = {
    #background to rgb(233, 238, 245)
    'background': '#303030 !important',
    'text': '#ffffff'
} 
color_discrete_map = {'Asia': '#636EFA', 'Africa': '#EF553B', 'Americas': '#00CC96',
    'Europe': '#AB63FA', 'Oceania': '#FFA15A'}


# change to app.layout if running as single page app instead
layout = html.Div(style={'backgroundColor': colors['background']},children=[
    html.H1('Global Suicide Data',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),
    #Add multiple line text 
    html.Div('''
        Suicide Rate vs GDP per Capita for different Continents from 1985 to 2005
    ''', style={
        'textAlign': 'center',
        'color': colors['text']}
    ),
    html.Div([
            ################### start of first row #######################   
                    dbc.Row(children=[
                        dbc.Col(
                            html.Div(["Select Continent"]),
                            width={"size": 4, "offset": 2},
                        ),
                        dbc.Col(
                            html.Div("Select Suicide in Hundredk Range"),
                            width={"size": 4, "offset": 2},
                        )
                 ], className='ml-2 mb-2',justify="center",),
                dbc.Row(children=[
                    dbc.Col(children=[
                    dcc.Dropdown(id='cont_dropdown',
                                options=[{'label': i, 'value': i}
                                        for i in country_names],
                                value=country_names,
                                multi=True,
                                style={
                                    'marginLeft' : '10px',
                                    'color': '#1c1818',
                                }
                    )
                    ], className='ml-5 mb-2'),  
                    dbc.Col(dbc.Col(children=[
                             dcc.RangeSlider(id='suicide_range_slider',
                                min=0,
                                max=600,
                                value=[0,600],
                                step= 10,
                                marks={
                                    0: '0',
                                    # 50: '50',
                                    300: '300',
                                    600: '600',
                                },

                                )
                                ], className='ml-2 mb-2'),
                        ),
                    ]),



            ################### End of first row #######################  
                dbc.Row([
                dbc.Col(html.Div(children=
                    [
                        dcc.Graph(id='bubble_graph',
                        responsive=True,
                        style={
                            "width": "100%",
                            "height": "100%",
                            'marginLeft' : '10px',
                        },),               
                    ],className=''),className='col-12 col-sm-12 col-md-12 ml-5 mt-3'),

                ],className='pt-2 pb-2',
                    style={"width": "100%",
                    "height": "500px",
                    "display": "inline-block",
                    "padding-left": "15px",
                    "padding-right": "15px",
                    "overflow": "hidden",
                    "align":"center"}),

            ################### End of second row #######################    
                dbc.Row([
                dbc.Col(html.Div(children=
                    [
                        dcc.Dropdown(id='y_dropdown',
                        options=[                    
                            {'label': 'Suicide in Hundredk', 'value': 'sucid_in_hundredk'},
                            {'label': 'Population', 'value': 'population'},
                            {'label': 'GDP per Captia', 'value': 'gdp_per_capita'}],
                        value='sucid_in_hundredk',
                        style={'width':'50%',
                               'color': '#1c1818',},
                        ),               
                    ],className='ml-3 mr-3 mt-3'),className='col-11 col-sm-12 col-md-12'),

            ], 
            className='text-center pb-3 ml-3',
            style={
                'marginLeft' : '10px',
                'textAlign': 'center',
                'color': '#00000',
            },),

            ################### End of third row #######################   
                    dbc.Row([
                        dbc.Col(
                            html.Div(children=
                            [
                                html.Div([
                                    dcc.Graph(id='map_chart')
                                ],className=' mr-3 ml-3',),    
                            ]),className='col-6 col-sm-6 col-md-6'),
                            dbc.Col(html.Div(children=
                            [
                                html.Div([
                                    dcc.Graph(id='line_chart',)
                                ],className=' mr-3 ml-3',
                                style={}),    
                            ]),className='col-6 col-sm-6 col-md-6'),
                    ],className='text-center pb-3',align="center",
                    style={
                        'marginLeft' : '10px',
                        'marginRight' : '10px',
                    }),

            ################### End of fourth row #######################         
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
])
@app.callback(
    Output(component_id='bubble_graph', component_property='figure'),
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='suicide_range_slider', component_property='value')]
)
def update_graph(selected_cont,rangevalue):
    if not selected_cont:
        return dash.no_update
    data =[]
    d = loc_data[(loc_data['sucid_in_hundredk'] >= rangevalue[0]) & (loc_data['sucid_in_hundredk'] <= rangevalue[1])]
    # d = gapminder[(gapminder['population'] >= rangevalue[0]) & (gapminder['population'] <= rangevalue[1])]
    for j in selected_cont:
            data.append(d[d['country'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=cols)
    df=df.infer_objects()
    # print(df.columns)
    mask = df.country.isin(country_names)
    tempdf = df[mask]
    ndf = tempdf.groupby(['year','country_code','continent','country']).agg(sucid_in_hundredk = ('sucid_in_hundredk','sum'),
    suicides = ('suicides','sum'),
    population = ('population','sum'),
    gdp_per_capita = ('gdp_per_capita','sum'),
    ).reset_index()
    print('\n\n ################## final data : ################## \t \n\n', ndf['country'].unique())
    scat_fig = px.scatter(data_frame=ndf, x="gdp_per_capita", y="sucid_in_hundredk",
                size="sucid_in_hundredk", color="country",hover_name="country",
                color_discrete_map=color_discrete_map, 
                animation_frame="year",animation_group="country",
                size_max=80, range_x=[0,1100000], range_y=[0,600],
                labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
                'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita',})
    scat_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    return scat_fig



@app.callback(
    [Output(component_id='map_chart', component_property='figure'),
    Output(component_id='line_chart', component_property='figure')],
    [Input(component_id='cont_dropdown', component_property='value'),
    Input(component_id='suicide_range_slider', component_property='value'),
    Input(component_id='y_dropdown', component_property='value')]
)
def update_map(selected_cont,rangevalue,yvar):
    if not (selected_cont or rangevalue or yvar):
        return dash.no_update
    d = loc_data[(loc_data['sucid_in_hundredk'] >= rangevalue[0]) & (loc_data['sucid_in_hundredk'] <= rangevalue[1])]
    data =[]
    for j in selected_cont:
            data.append(d[d['country'] == j])
    df = pd.DataFrame(np.concatenate(data), columns=loc_cols)
    df=df.infer_objects()
    # print(df.columns)
    mask = df.country.isin(country_names)
    tempdf = df[mask]
    ndf = tempdf.groupby(['year','country_code','continent','country']).agg(sucid_in_hundredk = ('sucid_in_hundredk','sum'),
     suicides = ('suicides','sum'),
     population = ('population','sum'),
     gdp_per_capita = ('gdp_per_capita','sum'),
     ).reset_index()
    # print('\n\n ################## final data : ################## \t \n\n', ndf)
    map_fig= px.choropleth(ndf,locations="country_code", color=ndf[yvar],
        hover_name=ndf[yvar],hover_data=['continent','sucid_in_hundredk','gdp_per_capita'],animation_frame="year",    
        color_continuous_scale='Turbo',range_color=[ndf[yvar].min(), ndf[yvar].max()],
        labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
                'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita',})
    map_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)')

    line_fig = px.line(data_frame=ndf, 
        x="year",  y = ndf[yvar] , color='country',line_group="country", 
        hover_data=['sucid_in_hundredk','year'],
        # Add bold variable in hover information
        hover_name=ndf[yvar],color_discrete_map=color_discrete_map,
        # change labels
        labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
                'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita',})
    line_fig.update_layout(plot_bgcolor='rgb(233, 238, 245)',
        paper_bgcolor='rgb(233, 238, 245)')
        
    return [map_fig, line_fig]