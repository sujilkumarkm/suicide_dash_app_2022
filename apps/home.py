import dash
from dash import html
import dash_bootstrap_components as dbc
from app import app

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
                dbc.Row([
           dbc.Col(dbc.CardImg(src=app.get_asset_url('/wall_paper.jpg'), className = 'text-center'),
            style={"maxWidth": "100%"})
        ]),
        dbc.Row([
            #Header span the whole row
            #className: Often used with CSS to style elements with common properties.
            # dbc.Col(html.Img(src = '/assets/wall_paper.jpg', height= "500px", className="text-center")),
            dbc.Col(html.H1("Welcome DKIT Gaelic dashboard", className="text-center")
                    , className="mb-5 mt-5")            
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='This project is created to dive deep inot the data of Gaelic games held between different teams in ireland. The purpose of this project to study and understands different trends or patterns in the data for the betterment of young developing gelic player community. Python Dash and plotly are used to make visualisation from the dataset. This project is conducted as part of the coninueous assesment held in Dundalk Institute of Technology as part of Msc in Data Analysis'
                                     )
                    , className="mb-4")
            ]),

        dbc.Row([
            dbc.Col(html.H5(children='Gaelic games (Irish: Cluichí Gaelacha) are sports played in Ireland under the auspices of the Gaelic Athletic Association (GAA). They include Gaelic football, hurling, Gaelic handball, and rounders. Womens versions of hurling and football are also played: camogie, organised by the Camogie Association of Ireland, and ladies Gaelic football, organised by the Ladies Gaelic Football Association.'
                )
                    , className="mb-5")
        ]),

        dbc.Row([
            # 2 columns of width 6 with a border
            dbc.Col(dbc.Card(children=[html.H3(children='Abount Me',
                                               className="text-center",id='aboutme'),
                                             dbc.Col(html.H5(children='Motivated, teamwork-oriented, and responsible Data Analyst with       significant experience in increasıng Comprehension of report and presentations by the average professional. Highly educated, possessing a Bachelors, a Masters, and 6 years professional         experience in IT. Bilingual in English, Malayalam, and Tamil, with an intermediate understanding of Hindi'
                )
                                     , className="mb-5",style={"minHeight": "100px"}),
                                    dbc.Button("Connect  Sujil Kumar K.M",
                                    href="https://www.linkedin.com/in/sujil/", target="_blank",
                                    # color="primary",
                                    className="mt-3 btn btn-danger"),
                                    
                                       ],
                             
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4"),

            dbc.Col(dbc.Card(children=[html.H3(children='About DKIT',
                                               className="text-center"),
                                       dbc.Col(html.H5(children='Dundalk Institute of Technology is an institute of technology based in Dundalk within County Louth, Ireland. Created as Dundalk Regional Technical College, students were first enrolled in the college in 1971 and was later re-defined as an institute of technology in January, 1998.'
                )
                                     , className="mb-5",style={"minHeight": "100px"}),
                                       dbc.Button("Dundalk Institute of Technology (DKIT)",
                                                  href="https://dkit.ie", target="_blank",
                                                  color="primary",
                                                  className="mt-3 btn btn-success"),
                                      
                                       ],
                             body=True, color="dark", outline=True)
                    , width=6, className="mb-4")

        ], className="mb-5"),
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