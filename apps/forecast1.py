# ARIMA MODEL

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

layout = html.Div([
################### start of first row #######################   
                html.H1('SARIMA Model Forecast',)
],className='text-center')