
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


layout = html.Div([
################### start of first row #######################   
                html.H5('Suicide Statistics Countrywise',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),
                dbc.Row(children=[
                    dbc.Col(children=[
                    html.Label('Select Countries'),
                    dbc.Col(html.Div(children=[
                    dcc.Graph(id="distance_graphssss")],className='ml-3 mt-3')
                    ,className='col-6 col-sm-6 col-md-6'),
                    ], className='ml-2 mb-2'),  

                    ]),



])

@app.callback(
    [Output(component_id='distance_graphssss', component_property='figure'),
     
    
     ],
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
    # fig = px.scatter(dff[mask], 
    # x="population", y="sucid_in_hundredk", color="country", size='population',
    #              hover_name="sex", size_max=60)
    mask3 = dfff.country.isin(country_names)

    fig3 = px.scatter(
            data_frame=dfff[mask3],
            x="sucid_in_hundredk",
            y="gdp_per_capita",
            hover_data=['country'],
            text="country",labels={"sucid_in_hundredk": "Suicide per hundred thousand","gdp_per_capita": "GDP Per capita",})
    return [fig3]





