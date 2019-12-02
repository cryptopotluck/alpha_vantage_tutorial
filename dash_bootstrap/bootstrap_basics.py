"""
A simple app demonstrating how to manually construct a navbar with a customised
layout using the Navbar component and the supporting Nav, NavItem, NavLink,
NavbarBrand, and NavbarToggler components.
Requires dash-bootstrap-components 0.3.0 or later
"""
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import requests, base64
from io import BytesIO
import dash_core_components as dcc
import plotly.graph_objs as go
from collections import Counter

PLOTLY_LOGO = "https://potluckspaces.sfo2.cdn.digitaloceanspaces.com/static/img/contentcreator.png"

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# try running the app with one of the Bootswatch themes e.g.
# app = dash.Dash(external_stylesheets=[dbc.themes.JOURNAL])
# app = dash.Dash(external_stylesheets=[dbc.themes.SKETCHY])


"""Navbar"""
#dropdown Items

# make a reuseable navitem for the different examples
nav_item = dbc.NavItem(dbc.NavLink("Dash Udemy Course", href="https://www.udemy.com/course/plotly-dash/?referralCode=16FC11D8981E0863E557"))

# make a reuseable dropdown for the different examples
dropdown = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("Youtube Channel", href='https://www.youtube.com/channel/UC-pBvv8mzLpj0k-RIbc2Nog?view_as=subscriber'),
        dbc.DropdownMenuItem("Potluck App", href='https://cryptopotluck.com/'),
        dbc.DropdownMenuItem(divider=True),
        dbc.DropdownMenuItem("Project Github", href='https://github.com/cryptopotluck/alpha_vantage_tutorial'),
        dbc.DropdownMenuItem("Plotly / Dash", href='https://dash.plot.ly/'),
        dbc.DropdownMenuItem("Dash Bootstrap", href='https://dash-bootstrap-components.opensource.faculty.ai/'),
    ],
    nav=True,
    in_navbar=True,
    label="Important Links",
)

#Navbar Layout
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("CryptoPotluck", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="https://plot.ly",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_item,
                     dropdown,
                     ], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5",
)

#####################################################################################
"""App Components"""
#Dropdown App
def enconde_image(image_url):
    buffered = BytesIO(requests.get(image_url).content)
    image_base64 = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + image_base64


DropdownApp = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Houston', 'value': 'TX'},
            {'label': 'San Francisco', 'value': 'SF'}
        ],
        value='NYC',
        placeholder="Select a city",
    ),
    html.Div(id='output-container')
])

#Textarea App
def transform_value(value):
    return 10 ** value


TextApp = html.Div([
    html.H1('Common Words Graph'),
    dcc.Graph(id='txt-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Textarea(
        id='txt',
        placeholder='Common Words...',
        value='',
        style={'width': '100%'}
    ),
    html.Div(id='text-output-container', style={'margin-top': 20})
])

#Slider
SliderApp = html.Div([
    html.H1('Square Root Slider Graph'),
    dcc.Graph(id='slider-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Slider(
        id='slider-updatemode',
        marks={i: '{}'.format(i) for i in range(20)},
        max=20,
        value=2,
        step=1,
        updatemode='drag',
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])

"""Body Components"""
#Cards
cardOne = dbc.Card(
    [
        dbc.CardImg(src="https://i.imgur.com/JnUeE7g.png", top=True),
        dbc.CardBody(
            [
                html.H4("Dropdown Components & Images", className="card-title"),
                html.P(
                    "We learn how to create dropdown components & render different types of image types within dash applications.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="open",  color='warning', style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Modal"),
                        dbc.ModalBody(DropdownApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="close", className="ml-auto")
                        ),
                    ],
                    id="modal",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

cardTwo = dbc.Card(
    [
        dbc.CardImg(src="https://i.imgur.com/mItJUKG.png", top=True),
        dbc.CardBody(
            [
                html.H4("Sq Root Slider", className="card-title"),
                html.P(
                    "This simple line graph highlights the slider"
                    "as it calculates the sq root based off the two numbers selected by the slider",
                    className="card-text",
                ),
                dbc.Button("Open App", id="opentwo", color='primary', style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Modal"),
                        dbc.ModalBody(SliderApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="closetwo", className="ml-auto")
                        ),
                    ],
                    id="modaltwo",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

cardThree = dbc.Card(
    [
        dbc.CardImg(src="https://i.imgur.com/a9rphkb.png", top=True),
        dbc.CardBody(
            [
                html.H4("Word Distribution Counter", className="card-title"),
                html.P(
                    "This App will break down paragraphs or long articles & count & map the word distribution "
                    "providing a powerful tool for figuring out keywords.",
                    className="card-text",
                ),
                dbc.Button("Open App", id="openthree", color='success', style={'margin': 'auto', 'width': '100%'}),
                dbc.Modal(
                    [
                        dbc.ModalHeader("Modal"),
                        dbc.ModalBody(TextApp),
                        dbc.ModalFooter(
                            dbc.Button("Close", id="closethree", className="ml-auto")
                        ),
                    ],
                    id="modalthree",
                ),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_content = [
    dbc.CardHeader("Dash-Bootstrap-Components Tutorial"),
    dbc.CardBody(
        [
            html.H5("Styling Made Simple", className="card-title"),
            html.P(
                "This tutorial we will learn the fundamentals to an awesome addition to dash that will allow us to integrate bootstap functionality into our projects & we will embed three of our apps we developed from the Udemy course.",
                className="card-text",
            ),
        ]
    ),
]

"""Body"""
#rows
row = html.Div(
    [
        dbc.Row(html.Img(src="https://i.imgur.com/dHZLL1a.png", style={'float': 'right', 'clear': 'right', 'margin-left': '19%', 'width': '80vw', 'height': '30vh'})),
        dbc.Row(dbc.Col(html.Div(dbc.Col(dbc.Card(card_content, color="dark", inverse=True)),))),
        dbc.Row(html.P('')),
        dbc.Row(
            [
                dbc.Col(html.Div(cardOne)),
                dbc.Col(html.Div(cardTwo)),
                dbc.Col(html.Div(cardThree)),
            ],
            style={'margin': 'auto', 'width': '80vw'}
),
    ]
)
#####################################################################################

"""Layout"""

app.layout = html.Div(
    [navbar, row]
)


"""Apps Functions"""
#dropdown App
@app.callback(
    Output('output-container', 'children'),
    [Input('my-dropdown', 'value')])
def update_output(value):
    NYC_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fcincoveces.files.wordpress.com%2F2011%2F08%2Fnycpan2.jpg&f=1&nofb=1')
    TX_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.sparefoot.com%2Fmoving%2Fwp-content%2Fuploads%2F2015%2F12%2FThinkstockPhotos-480535456-1-1.jpg&f=1&nofb=1')
    SF_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.hotelgsanfrancisco.com%2Fassets%2Fthemes%2Fhotelgsanfrancisco%2Fimg%2FHotelG-map.jpg&f=1&nofb=1')
    if value == 'NYC':
        return html.Div(html.Img(src=NYC_img.decode(), style={'width': '100%', 'height':'400px'}))
    elif value == 'TX':
        return html.Div(html.Img(src=TX_img.decode(), style={'width': '100%', 'height':'400px'}))
    elif value == 'SF':
        return html.Div(html.Img(src=SF_img.decode(), style={'width': '100%', 'height':'400px'}))

#Slider App
@app.callback([
               Output('slider-graph', 'figure'),
               Output('updatemode-output-container', 'children')
               ],
              [Input('slider-updatemode', 'value')])
def display_value(value):


    x = []
    for i in range(value):
        x.append(i)

    y = []
    for i in range(value):
        y.append(i*i)

    graph = go.Scatter(
        x=x,
        y=y,
        name='Manipulate Graph'
    )
    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(range=[min(x), max(x)]),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}, f'Value: {round(value, 1)} Square: {value*value}'

#Text App
@app.callback(
               Output('txt-graph', 'figure')
               ,
              [Input('txt', 'value')])
def display_value(value):

    word_list = value.split()

    word_dic=Counter(word_list)
    x = list(word_dic.keys())
    y = list(word_dic.values())

    graph = go.Bar(
        x=x,
        y=y,
        name='Manipulate Graph',
        type='bar',
        marker=dict(color='lightgreen')
    )

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type="category"),
        yaxis=dict(range=[min(y), max(y)]),
        font=dict(color='white'),

    )
    return {'data': [graph], 'layout': layout}

#module One
@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open
#Module Two
@app.callback(
    Output("modaltwo", "is_open"),
    [Input("opentwo", "n_clicks"), Input("closetwo", "n_clicks")],
    [State("modaltwo", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open

#Module Three
@app.callback(
    Output("modalthree", "is_open"),
    [Input("openthree", "n_clicks"), Input("closethree", "n_clicks")],
    [State("modalthree", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# we use a callback to toggle the collapse on small screens
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)