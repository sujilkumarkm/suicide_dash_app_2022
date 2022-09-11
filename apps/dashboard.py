
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from pytz import country_names
import mysql.connector as connection

#data for the Suicide plots
# mydb = connection.connect(host="204.93.172.126", database = 'dkitienarayam_db',user="dkitienarayam_admin", passwd="Unnikuttan@1991",use_pure=True)
# query = "Select * from suicides;"

df = pd.read_csv("assets/processed_data/output.csv")
# df = df.iloc[10:1000]
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app

{'Albania': '#000000', 'Austria': '#FFFF00', 'Belgium': '#1CE6FF',
    'Bosnia and Herzegovina': '#FF34FF','Bulgaria': '#FF4A46', 'Croatia': '#008941',
    'Czech Republic': '#006FA6', 'Denmark': '#A30059', 'Finland': '#FFDBE5',
    'France': '#7A4900', 'Germany': '#0000A6', 'Greece': '#63FFAC', 'Hungary': '#B79762',
    'Iceland': '#8FB0FF', 'Ireland': '#004D43','Italy': '#997D87', 'Montenegro': '#5A0007',
    'Netherlands': '#809693', 'Norway': '#FEFFE6', 'Poland': '#1B4400','Portugal': '#4FC601',
    'Romania': '#3B5DFF', 'Serbia': '#4A3B53', 'Slovak Republic': '#FF2F80',
    'Slovenia': '#61615A','Spain': '#BA0900', 'Sweden': '#6B7900', 'Switzerland': '#00C2A0',
    'Turkey': '#FFAA92','United Kingdom': '#FF90C9'}

colorscale=[[0.0, "rgb(165,0,38)"],
                [0.1111111111111111, "rgb(215,48,39)"],
                [0.2222222222222222, "rgb(244,109,67)"],
                [0.3333333333333333, "rgb(253,174,97)"],
                [0.4444444444444444, "rgb(254,224,144)"],
                [0.5555555555555556, "rgb(224,243,248)"],
                [0.6666666666666666, "rgb(171,217,233)"],
                [0.7777777777777778, "rgb(116,173,209)"],
                [0.8888888888888888, "rgb(69,117,180)"],
                [1.0, "rgb(49,54,149)"]]

layout = html.Div([
################### start of first row #######################   
                html.H1('Suicide Statistics Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                        dbc.Col(
                            html.Div(["Select Continent"]),
                            width={"size": 4, "offset": 2},
                        ),
                        dbc.Col(
                            html.Div("Select Suicide Range"),
                            width={"size": 4, "offset": 2},
                        )
                ], className='ml-2 mb-2',justify="center",),
                dbc.Row(children=[
                    dbc.Col(children=[
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
                                dcc.RangeSlider(id='suicides_slider',
                                    min=0,
                                    max=180,
                                    value=[0,180],
                                    step= 1,
                                    marks={
                                        0: '0',
                                        50: '50',
                                        100: '100',
                                        178: '178',
                                    },
                                )
                                ],
                                ),
                                ],className='pb-2')
                        ),
                    ],style={
                        'marginLeft' : '10px',
                    }),

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
            style={
                'marginLeft' : '10px',
                'marginRight': '10px',
            }),

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
            style={
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

@app.callback(
    [Output(component_id='distance_graph', component_property='figure'),
     Output(component_id='count_dist_graph', component_property='figure'),
     Output(component_id='shot_graph', component_property='figure'),
     Output(component_id='scat_graph', component_property='figure'),],
    [Input(component_id='country_drop', component_property='value'),
     Input(component_id='suicides_slider', component_property='value'),
    ]
)
def update_line_chart(country_names, range_chosen):
    if not (country_names or range_chosen):
        return dash.no_update
    d = df[(df['sucid_in_hundredk'] >= range_chosen[0]) & (df['sucid_in_hundredk'] <= range_chosen[1])]
    data =[]
    for j in country_names:
            data.append(d[d['country'] == j])
    dff = pd.DataFrame(np.concatenate(data), columns=columnss)
    dff=dff.infer_objects()
    mask = dff.country.isin(country_names)
    tempdf = dff[mask]
    ndf = tempdf.groupby(['year','country_code','continent','country','sex']).agg(sucid_in_hundredk = ('sucid_in_hundredk','sum'),
     suicides = ('suicides','sum'),
     population = ('population','sum'),
     gdp_per_capita = ('gdp_per_capita','sum'),
     ).reset_index()
    fig= px.choropleth(ndf,               
            locations="country_code", color="suicides",
            hover_name="country",  
            animation_frame="year",
            labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
                    'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita',})     
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False,title="World Total Suicides over time", title_x=0.5)

    ndf1 = ndf.groupby(['country']).sucid_in_hundredk.mean().nlargest(10)
    ndf1 = pd.DataFrame({'country':ndf1.index, 'sucid_in_hundredk':ndf1.values})
    fig2 = px.bar(ndf1, x="sucid_in_hundredk", y="country", orientation='h',color='country',color_continuous_scale='Bluered_r', hover_name="country",
    labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
    'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita',})
    fig2.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False,title="Top ten countries in suicide per hundredk", title_x=0.5)
    # start of barchart code
    female_data = pd.DataFrame(tempdf.groupby('sex').get_group('female').groupby('age').suicides.sum())
    sex_female = 'female'
    female_data['sex'] = sex_female
    # print('\n\n ################## female data : ##################\t \n\n', female_data)
    
    male_data = pd.DataFrame(tempdf.groupby('sex').get_group('male').groupby('age').suicides.sum())
    sex_male = 'male'
    male_data['sex'] = sex_male
    # print('\n\n ################## male data : ################## \t \n\n', male_data)
    total_sex = female_data.append(male_data)
    # print('\n\n ################## total data : ################## \t \n\n', total_sex)
    
    ndf = total_sex.groupby(['sex','age']).agg(
    suicides = ('suicides','sum'),
    # age = ('age','sum'),
    ).reset_index()
    # print('\n\n ################## final data : ################## \t \n\n', ndf)
    fig1 = px.bar(ndf, x="age", color="sex",
             y='suicides',
             barmode='relative',
             labels={'sucid_in_hundredk':'Suicides Per Hundredk','year':'Year','continent':'Continent',
                    'country':'Country','suicides':'Suicide', 'population':'Population','gdp_per_capita':'GDP per Capita','sex':'Sex','age':'Age',},)
    fig1.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=True,title="Gender and Total Suicide Age-wise", title_x=0.5,  xaxis={'categoryorder':'total descending'})
    # end of barchart code
    
    dfff=dff.groupby(["country"], as_index=False)[["sucid_in_hundredk","gdp_per_capita"]].mean()
    mask3 = dfff.country.isin(country_names)

    fig3 = px.scatter(
            data_frame=dfff[mask3],
            x="sucid_in_hundredk",
            y="gdp_per_capita",
            hover_data=['country'],
            text="country",labels={"sucid_in_hundredk": "Suicide per hundred thousand","gdp_per_capita": "GDP Per capita","country":"Country Name"})
    fig3.update_layout(uniformtext_minsize=8, uniformtext_mode='hide',
        plot_bgcolor='rgb(233, 238, 245)',paper_bgcolor='rgb(233, 238, 245)',
        showlegend=False, title_x=0.5)
    return [fig, fig1, fig3, fig2]





