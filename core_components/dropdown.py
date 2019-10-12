import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import requests, base64
from io import BytesIO


app = dash.Dash()

def enconde_image(image_url):
    buffered = BytesIO(requests.get(image_url).content)
    image_base64 = base64.b64encode(buffered.getvalue())
    return b'data:image/png;base64,' + image_base64


app.layout = html.Div([
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


@app.callback(
    Output('output-container', 'children'),
    [Input('my-dropdown', 'value')])
def update_output(value):
    NYC_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fcincoveces.files.wordpress.com%2F2011%2F08%2Fnycpan2.jpg&f=1&nofb=1')
    TX_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.sparefoot.com%2Fmoving%2Fwp-content%2Fuploads%2F2015%2F12%2FThinkstockPhotos-480535456-1-1.jpg&f=1&nofb=1')
    SF_img = enconde_image('https://proxy.duckduckgo.com/iu/?u=http%3A%2F%2Fwww.hotelgsanfrancisco.com%2Fassets%2Fthemes%2Fhotelgsanfrancisco%2Fimg%2FHotelG-map.jpg&f=1&nofb=1')
    if value == 'NYC':
        return html.Div(html.Img(src=NYC_img.decode(), style={'width': '500px', 'height':'400px'}))
    elif value == 'TX':
        return html.Div(html.Img(src=TX_img.decode(), style={'width': '500px', 'height':'400px'}))
    elif value == 'SF':
        return html.Div(html.Img(src=SF_img.decode(), style={'width': '500px', 'height':'400px'}))


if __name__ == '__main__':
    app.run_server(debug=True)