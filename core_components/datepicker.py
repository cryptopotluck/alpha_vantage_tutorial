import dash
import dash_html_components as html
import dash_core_components as dcc, dash_table
from dash.dependencies import Input, Output
from datetime import datetime as dt
from _alpha_vantage.key import api_key
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.timeseries import TimeSeries





external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.DatePickerSingle(
        id='date-picker-range',
        date=dt(2019, 5, 3),
    ),
    html.Div(id='date-content')
])

api_key = api_key
period = 60
ts = TimeSeries(key=api_key, output_format='pandas')



@app.callback(Output('date-content', 'children'),
              [Input('date-picker-range', 'date')])
def render_content(date):
    data_ts = ts.get_daily(symbol='fb', outputsize='full')
    price_df = data_ts[0][period::]
    date = dt.strptime(date, '%Y-%m-%d')
    price_table = price_df.index > date

    return html.Div(dash_table.DataTable(
            id='table',
            columns=[{'name': i, 'id': i} for i in price_df[price_table].columns],
            data=price_df[price_table].to_dict('rows'),
            style_cell={'width': '300px',
                        'height': '30px',
                        'textAlign': 'left'}
        ))




if __name__ == '__main__':
    app.run_server(debug=True)

166.23
11.4
166.23