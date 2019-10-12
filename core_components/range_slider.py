import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic
def transform_value(value):
    return 10 ** value


app.layout = html.Div([
    html.H1('Subtract'),
    dcc.RangeSlider(
        id='range_slider',
        min=0,
        max=30,
        value=[20, 10],
    ),
    html.Div(
        html.Div(id='solution', style={'margin-top': 20}),
    )

])


@app.callback([
                Output('solution', 'children'),
               ],
              [
                  Input('range_slider', 'value')
              ])
def display_value(value):
    return [f'You have selected {value[1]} - {value[0]} = {value[1]-value[0]}']


if __name__ == '__main__':
    app.run_server(debug=True)