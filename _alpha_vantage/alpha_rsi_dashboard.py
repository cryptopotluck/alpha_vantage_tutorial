import pandas as pd
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash()

app.layout = html.Div([
    html.Link(
            rel='stylesheet',
            href='https://codepen.io/chriddyp/pen/bWLwgP.css'
        ),
    dcc.Input(id='input-box', value='', type='text', placeholder='Enter a Stock symbol', ),
    html.Button('Submit', id='button'),
    html.Div(),
    html.P('5 Calls Per Min'),
    dcc.Graph(
        id='candle-graph', animate=True, style={"backgroundColor": "#1a2d46", 'color':'#ffffff'},),
    html.Div([
            html.P('Developed by: ', style={'display': 'inline', 'color' : 'white'}),
            html.A('Austin Kiese', href='http://www.austinkiese.com'),
            html.P(' - ', style={'display': 'inline', 'color' : 'white'}),
            html.A('cryptopotluck@gmail.com', href='mailto:cryptopotluck@gmail.com')
        ], className="twelve columns",
            style={'fontSize': 18, 'padding-top': 20}

        )
])

api_key = ''
period = 60
ts = TimeSeries(key=api_key, output_format='pandas')
ti = TechIndicators(key=api_key, output_format='pandas')

@app.callback(Output('candle-graph', 'figure'),
              [Input('button', 'n_clicks')],
              [State('input-box', 'value')])
def update_layout(n_clicks, input_value):

    #Getting Dataframes Ready
    data_ts = ts.get_intraday(symbol=input_value.upper(), interval='1min', outputsize='full')
    data_ti, meta_data_ti = ti.get_rsi(symbol=input_value.upper(), interval='1min', time_period=period, series_type='close')

    df = data_ts[0][period::]

    df.index = pd.Index(map(lambda x: str(x)[:-3], df.index))

    df2 = data_ti

    total_df = pd.concat([df, df2], axis=1, sort=True)

    #Breaking Down Datafames

    opens = []
    for o in total_df['1. open']:
        opens.append(float(o))

    high = []
    for h in total_df['2. high']:
        high.append(float(h))

    low = []
    for l in total_df['3. low']:
        low.append(float(l))

    close = []
    for c in total_df['4. close']:
        close.append(float(c))

    rsi_offset = []

    for r, l in zip(total_df['RSI'], low):
        rsi_offset.append(l-(l / r))

    #SELL SCATTER
    high_rsi_value = []
    high_rsi_time = []

    for value, time, l in zip(total_df['RSI'], total_df.index, low):
        if value > 60:
            high_rsi_value.append(l-(l/value))
            high_rsi_time.append(time)

    #BUY SCATTER
    low_rsi_value = []
    low_rsi_time = []

    for value, time, l in zip(total_df['RSI'], total_df.index, low):
        if value < 35:
            low_rsi_value.append(l - (l / value))
            low_rsi_time.append(time)


    scatter = go.Scatter(
        x=high_rsi_time,
        y=high_rsi_value,
        mode='markers',
        name='Sell'
    )
    scatter_buy = go.Scatter(
        x=low_rsi_time,
        y=low_rsi_value,
        mode='markers',
        name='Buy'
    )

    rsi = go.Scatter(
        x=total_df.index,
        y=rsi_offset,
    )

    BuySide = go.Candlestick(
        x=total_df.index,
        open=opens,
        high=high,
        low=low,
        close=close,
        increasing={'line': {'color': '#00CC94'}},
        decreasing={'line': {'color': '#F50030'}},
        name='candlestick'
    )
    data = [BuySide, rsi, scatter, scatter_buy]

    layout = go.Layout(
        paper_bgcolor='#27293d',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(type="category"),
        yaxis=dict(range=[min(rsi_offset), max(high)]),
        font=dict(color='white'),

    )
    return {'data': data, 'layout': layout}


if __name__ == '__main__':
    app.run_server(port=8085)


