import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import dash
from collections import Counter

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Use the following function when accessing the value of 'my-slider'
# in callbacks to transform the output value to logarithmic
def transform_value(value):
    return 10 ** value


app.layout = html.Div([
    html.H1('Common Words Graph'),
    dcc.Graph(id='txt-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color': '#ffffff'}),
    dcc.Textarea(
        id='txt',
        placeholder='Common Words...',
        value='',
        style={'width': '100%'}
    ),
    html.Div(id='updatemode-output-container', style={'margin-top': 20})
])


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


if __name__ == '__main__':
    app.run_server(debug=True)