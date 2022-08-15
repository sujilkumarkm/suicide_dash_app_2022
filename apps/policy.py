from dash import html
import dash_bootstrap_components as dbc
from app import app



layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H2("Privacy Policy", className="text-center")
                    , className="mb-2 mt-2 text-center",style={'justifyContent': 'center'})            
        ]),
        dbc.Row([
            dbc.Col(html.H5("The information we used for this project is strictly private, and nobody is permitted to use any of the materials posted on this website without first obtaining permission from DKIT. If someone accessed the DKIT data, they would be solely responsible for upholding all ethical standards. No one is allowed to use any information provided in the website without taking any consent from DKIT management. In case of any data misuse or breach that particular person will be responsible for the misuse of data. the data is completely confidential and it is collected from that particular source and we are obligated to keep it's confidentiality taking all the ethical considerations into account and for publishing this data online as part of the project we will make sure there is no data bridge dot please make sure to take consent before getting any source of information from the created this website only four academic research purposes and there is no other data privacy violation or threat made by the project. if you have any queries regarding this project please contact d00242726@student.dkit.ie for any support or queries regarding this work. This project is conducted under the supervision of Jack Mc Donnell from the School of Informatics and Creative Arts - DKIT ", className="text-center")
                    , className="mb-5 mt-5 text-center",style={'justifyContent': 'center'})            
        ]),
                 dbc.Row([
            # 2 columns of width 6 with a border
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

    ])
    ])
        
    ])
])