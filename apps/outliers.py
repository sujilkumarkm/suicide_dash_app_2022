
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pytz import country_names
import mysql.connector as connection

mydb = connection.connect(host="204.93.172.126", database = 'dkitienarayam_db',user="dkitienarayam_admin", passwd="Unnikuttan@1991",use_pure=True)
query = "Select * from suicides;"
df = pd.read_sql(query,mydb)
#data for the Suicide plots
df = pd.read_csv("assets/processed_data/output.csv")
countries = list(set(df.country.to_list()))
columnss=list(df.columns)
country_names = df['country'].unique()


from app import app


layout = html.Div([
################### start of first row #######################   
                html.H5('Data Integrity Check Via Periodic Outliers Detection',
                style={
                    'textAlign': 'center',
                    'color': '#00000',
                    }
                    ),

                dbc.Row(children=[


                    dbc.Col(html.Div(children=[
                            dcc.Graph(id="outlier_graph")
                        ],className='ml-3 mt-3')
                        ,className='col-6 col-sm-6 col-md-6'),



                    dbc.Col(html.Div(children=
                        [
                            html.Label('Select Country', className="pt-4 pb-4"),

                            ## drop down start    

                                                      dcc.Dropdown(id='country_dropdown',
                            options=countries,

                            value=countries[0],
                            style={'width':'70%',
                                'color': '#1c1818',},
                            ),

                            ## drop down ended


                            html.Label('Years', className="pt-4"),
                            dcc.RangeSlider(id='year_range',
                                min=1995,
                                max=2035,
                                value=[1995,2035],
                                step= 1,
                                marks={
                                    1995: '1995',
                                    1998: '1998',
                                    2001: '2001',
                                    2004: '2004',
                                    2007: '2007',
                                    2010: '2010',
                                    2013: '2013',
                                    2016: '2016',
                                    2019: '2019',
                                    2022: '2022',
                                    2025: '2025',
                                    2028: '2028',
                                    2031: '2031',
                                    2034: '2034',
                                    # 2035: '2035',
                                },
                            ),
                         
                        ], className="pt-2 pb-2"
                        )), 

                    ]
                    ,style={
                    'marginLeft' : '15px',}),
                
                html.Br(),html.Br(),html.Br(),
                ################### start of descriptiom row ##################
                dbc.Row(children=[
                        dbc.Col(
                            dbc.Col(html.H5(children='FOR YOUR INFORMATION:-',
                            className="text-center pt-2 pb-2"),
                            width={"size": 11},
                        ),
                )], className='ml-2 mb-2',justify="center",), 
                dbc.Row(children=[
                        dbc.Col(
                            html.Div(["Data integrity check is a very effective technique to find the outliers in the data. Periodic outlier detection was the technique used to identify the data integrity. An Unsupervised Machine Learning algorithm called as DB Scan is used to detect outliers. When new data is available from the database over time the relavance of this feature is effective in determining the data integrity"]),
                            width={"size": 11},
                        ),
                ], className='ml-2 mb-2',justify="center",), 
                html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
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
            ),
                ########################### End of Footer #########################

])

@app.callback(
    [
        Output(component_id='outlier_graph', component_property='figure'),
     ],
    [
        Input(component_id='country_dropdown', component_property='value'),
        Input(component_id='year_range', component_property='value'),
    ]
)


def update_line_chart(country_dropdown, year_range):
    if not (country_dropdown or year_range):
        return dash.no_update
    possible_years = [str(y) for y in range(year_range[0], year_range[1])]

    raw_data = df
    outliers = pd.read_csv("assets/processed_data/outliers.csv")
    
    raw_data = raw_data[["year","sucid_in_hundredk", "country"]]
    outliers = outliers[["year","sucid_in_hundredk","country"]]

    raw_data["year_of_focus"] = raw_data.year.apply(lambda x: str(x).split("-")[0])
    outliers["year_of_focus"] = outliers.year.apply(lambda x: str(x).split("-")[0])

    new_df = pd.DataFrame()
    new_df["year_of_focus"] = possible_years

    new_raw_df = pd.merge(new_df,raw_data, on = "year_of_focus", how = "left")
    new_outlier_df = pd.merge(new_df,outliers, on = "year_of_focus", how = "left")
    new_raw_df = new_raw_df[new_raw_df.country == country_dropdown]
    new_outlier_df = new_outlier_df[new_outlier_df.country == country_dropdown]

    new_outlier_df["outlier"] = "Outlier"
    print(new_outlier_df)
    print(new_raw_df)
    new_raw_df = pd.merge(new_raw_df,new_outlier_df, on = ["year_of_focus","sucid_in_hundredk","country"], how = "left")

    outliers_label = []
    for i in new_raw_df.outlier.to_list():
        if i == "Outlier":
            outliers_label.append("Outlier Point")
        else:
            outliers_label.append("Good Point")

    new_raw_df["Outlier Detection"] = outliers_label

    fig = px.scatter(
            data_frame=new_raw_df,
            y="sucid_in_hundredk",
            x="year_of_focus",
            color = "Outlier Detection",
            labels={"sucid_in_hundredk": "Suicide per hundred thousand","year_of_focus": "Year",})


    return [fig]





