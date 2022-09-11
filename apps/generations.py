
# import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash_table import DataTable, FormatTemplate
import pandas as pd
from dash.dependencies import Input, Output
import mysql.connector as connection

#data for the Suicide plots
# mydb = connection.connect(host="localhost", database = 'dkit',user="root", passwd="",use_pure=True)
# query = "Select * from suicides;"
# df = pd.read_sql(query,mydb)

# df = pd.read_csv("assets/processed_data/output.csv")
# # print(df)

# columnss=list(df.columns)
# country_names = df['country'].unique()
# cont_names = df['continent'].unique()

df = pd.read_csv("assets/processed_data/output.csv")
# df = pd.read_csv('/usr/local/share/datasets/df.csv')
# logo_link = '/assets/dkit_logo.png'
major_continent = list(df['continent'].unique())
large_tb = df.groupby(['country'])['sucid_in_hundredk'].agg(['sum', 'count', 'mean', 'median']).reset_index().rename(columns={'count':'Suicide Per HundredK', 'sum':'Total Suicides', 'mean':'Average Suicides Value', 'median':'Median Suicides Value'})
ecom_country = df.groupby('country')['sucid_in_hundredk'].agg('sum').reset_index(name='Total Suicides')
bar_fig_country = px.bar(ecom_country, x='Total Suicides', y='country', width=500, height=450, title='Total Suicides by country (Hover to filter the generation bar chart!)', custom_data=['country'], color='country', color_discrete_map={'United Kingdom':'lightblue', 'Germany':'orange', 'France':'darkblue', 'Australia':'green', 'Hong Kong':'red'})

money_format = FormatTemplate.money(2)
summery_col = ['Total Suicides', 'Average Suicides Value', 'Median Suicides Value']
# print(summery_col)
d_columns = [{'name':x, 'id':x} for x in large_tb.columns if x not in summery_col]
d_columns += [
    {'name':'Total Suicides', 'id':'Total Suicides', 
    'type':'numeric', 
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    },
    {'name':'Average Suicides Value', 'id':'Average Suicides Value', 
    'type':'numeric', 
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    },
    {'name':'Median Suicides Value', 'id':'Median Suicides Value', 
    'type':'numeric', 
    'format':money_format
     # Allow columns to be selected
    , 'selectable':True
    }]

# print(d_columns)

d_table = DataTable(
  			id='my_dt',
            columns=d_columns,
            data=large_tb.to_dict('records'),
            cell_selectable=False,
            sort_action='native',
  			# Make single columns selectable
            column_selectable='single'
            )
# print(d_table)
from app import app

layout = html.Div([
#   html.Img(src=logo_link, 
#         style={'margin':'30px 0px 0px 0px' }),
  html.H1('Suicide breakdowns'),
  html.Div(
    children=[
    html.Div(
        children=[
        html.H2('Controls'),
        html.Br(),
        html.H3('continent Select'),
        dcc.Dropdown(id='major_cat_dd',
        options=[{'label':continent, 'value':continent} for continent in major_continent],
            style={'width':'200px', 'margin':'0 auto'}),
        html.Br(), html.Br(), html.Br(),
        html.H3('generation Select'),
        dcc.Dropdown(id='minor_cat_dd',
            style={'width':'200px', 'margin':'0 auto'})
        ],
        style={'width':'350px', 'height':'360px', 'display':'inline-block', 'vertical-align':'top', 'border':'1px solid black', 'padding':'20px'}),
    html.Div(children=[
            html.H3(id='chosen_major_cat_title'),
            dcc.Graph(id='gen_line')
            ],
             style={'width':'700px', 'height':'380px','display':'inline-block', 'margin-bottom':'5px'}
             ),
    html.Br(), html.Br(), html.Br(),
    
    ]),
  
   html.Br(), html.Br(),
    # html.Div(
    #         d_table
    #     , style={'width':'1000px', 'height':'200px', 'margin':'10px auto', 'padding-right':'30px', 'color': '#00000', },
    #     ),
  html.Div(children=[
    #   dcc.Graph(id='scatter_compare'),
      html.Div(dcc.Graph(id='major_cat', figure=bar_fig_country), style={'display':'inline-block'}),
      html.Div(dcc.Graph(id='minor_cat'), style={'display':'inline-block'})
            ],
             style={'width':'1000px', 'height':'650px','display':'inline-block'}
             ),
  ],style={'text-align':'center', 'display':'inline-block', 'width':'100%'}
  )

# Create a callback triggered by selecting a column
@app.callback(
    Output('scatter_compare', 'figure'),
    Input('my_dt', 'selected_columns'))

def table_country(selected_columns):
    comparison_col = 'Total Suicides'
	
    # Extract comparison col using its index
    # if selected_columns:
    #     comparison_col = selected_columns[0]

    # scatter_fig = px.scatter(
    #     data_frame=large_tb,
    #     x='Suicide Per HundredK',
    #   	# Use comparison col in figure
    #     y=comparison_col,
    #     color='country',
    #     title=f'Suicide Per HundredK vs {comparison_col} by country'
    # )

    # return scatter_fig

@app.callback(
   Output('minor_cat_dd', 'options'),
   Output('chosen_major_cat_title', 'children'),
   Input('major_cat_dd', 'value'))

def update_dd(major_cat_dd):
    major_minor = df[['continent', 'generation']].drop_duplicates()
    relevant_minor = major_minor[major_minor['continent'] == major_cat_dd]['generation'].values.tolist()
    minor_options = [dict(label=x, value=x) for x in relevant_minor]

    if not major_cat_dd:
        major_cat_dd = 'ALL'
    
    major_cat_title = f'This is in the continent of : {major_cat_dd}'

    return minor_options, major_cat_title

@app.callback(
    Output('gen_line', 'figure'),
    Input('minor_cat_dd', 'value'))

def update_line(minor_cat):
    minor_cat_title = 'All'
    ecom_line = df.copy()
    if minor_cat:
        minor_cat_title = minor_cat
        ecom_line = ecom_line[ecom_line['generation'] == minor_cat]
    ecom_line = ecom_line.groupby('year')['sucid_in_hundredk'].agg('sum').reset_index(name='Total Suicides')
    line_graph = px.line(ecom_line, x='year',  y='Total Suicides', title=f'Total Suicides by Month for generation: {minor_cat_title}', height=350)
    
    return line_graph

@app.callback(
    Output('minor_cat', 'figure'),
    Input('major_cat', 'hoverData'))

def update_min_cat_hover(hoverData):
    hover_country = 'Australia'
    
    if hoverData:
        hover_country = hoverData['points'][0]['customdata'][0]

    minor_cat_df = df[df['country'] == hover_country]
    minor_cat_agg = minor_cat_df.groupby('generation')['sucid_in_hundredk'].agg('sum').reset_index(name='Total Suicides')
    ecom_bar_minor_cat = px.bar(minor_cat_agg, x='Total Suicides', y='generation', orientation='h', height=450, width=480,title=f'Suicide by generation for: {hover_country}')
    ecom_bar_minor_cat.update_layout({'yaxis':{'dtick':1, 'categoryorder':'total ascending'}, 'title':{'x':0.5}})

    return ecom_bar_minor_cat