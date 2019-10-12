from binance.client import Client
import plotly.offline as pyo
import plotly.graph_objs as go
import pandas as pd
from plotly_graphs.binance_api_keys import APIKey, SecretKey

client = Client(api_key=APIKey, api_secret=SecretKey)
pd.set_option('float_format', '{:f}'.format)


def grab_binance_ballance():
    account = client.get_account()
    clean_df = pd.DataFrame(account['balances'])
    for index, row in clean_df.iterrows():
        if float(row['free']) < 0.01:
            clean_df.drop(index, inplace=True)

    clean_df['asset'] = clean_df['asset'].astype(str) + 'BTC'
    clean_df.set_index('asset', inplace=True)
    clean_df = clean_df.drop('locked', axis=1)
    return clean_df


print(grab_binance_ballance())


# %%

def grab_btc_equivalent():
    prices = client.get_all_tickers()
    cleandf = pd.DataFrame(prices)
    cleandf.set_index('symbol', inplace=True)

    return cleandf


print(grab_btc_equivalent())


# %%

def grab_btc():
    prices = client.get_symbol_ticker(symbol='BTCTUSD')
    cleandf = pd.DataFrame(prices, index=[0])
    cleandf.set_index('symbol', inplace=True)
    cleandf = float(cleandf['price'][0])
    return cleandf


print(grab_btc())


# %%

def compare_BTC_equivalent_and_binance_balance():
    btc_symbol = grab_btc_equivalent()
    binance_ballance = grab_binance_ballance()
    btc_value = grab_btc()

    filtered_df = btc_symbol.join(binance_ballance)
    filtered_df = filtered_df.dropna()
    filtered_df[['price', 'free']] = filtered_df[['price', 'free']].astype(float)
    filtered_df['btc_value'] = filtered_df['price'] * filtered_df['free']
    filtered_df['usd_value'] = filtered_df['btc_value'].multiply(float(btc_value))
    filtered_df = filtered_df[filtered_df.usd_value > 3.00]
    return filtered_df


print(compare_BTC_equivalent_and_binance_balance())

# %%

df = compare_BTC_equivalent_and_binance_balance()

values = []

for marketcap in df['usd_value'].unique():
    values.append(int(marketcap))

labels = []
for name in df.index.unique():
    labels.append(str(name))

trace = go.Pie(labels=labels, values=values, domain={'x': [0, .48]}, hoverinfo='label+value', hole=0.4)

layout = go.Layout(
    title='Binance: Total Asset Breakdown',
    paper_bgcolor='black',
    titlefont={"size": 30, 'color': '#ffffff'},
    legend={"font": {"color": '#ffffff'}},
    annotations=[{"font": {
        "size": 20,
        "color": '#ffffff',

    },

        "showarrow": False,
        "text": "Portfolio",
        "x": 0.19,
        "y": 0.5}])

data = [trace]

fig = go.Figure(data=data, layout=layout)

pyo.plot(fig)

