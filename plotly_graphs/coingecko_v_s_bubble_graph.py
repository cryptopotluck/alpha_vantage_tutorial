from plotly.offline import plot
from pycoingecko import CoinGeckoAPI
from pandas import DataFrame as df
from plotly_graphs.image import encoded_image
cg = CoinGeckoAPI()


def getCurrency(name):
    data = cg.get_coins_markets(vs_currency='usd', ids=name, order='market_cap_desc', per_page='100', page='1',
                                price_change_percentage='1h')
    return data[0]


def getALL():
    currency = ['civic', 'dogecoin', 'true-usd', 'ripple']
    allcoins = []

    for coin in currency:
        result = getCurrency(coin)

        allcoins.append(result)
        allcoins.sort(key=lambda c: c['market_cap_rank'])

    return allcoins


dataframe = df(getALL())
dataframe.set_index('symbol', inplace=True)


colors = ['blue', 'orange', 'green', 'red']

opt = []
opts = []
for i in range(0, len(colors)):
    opt = dict(
        target = dataframe['name'][[i]].unique(), value = dict(marker = dict(color = colors[i]))
    )
    opts.append(opt)

data = [dict(
  type = 'scatter',
  mode = 'markers',
  x = dataframe['circulating_supply'],
  y = dataframe['total_volume'],
  text = dataframe['name'],
  hoverinfo = 'text',
  opacity = 0.8,
  marker = dict(
      size = dataframe['total_volume'] /10000 ,
      sizemode = 'area',
  ),
  transforms = [
   dict(
        type = 'groupby',
        groups = dataframe['name'],
        styles = opts
      )
    ]
)]

layout = dict(
    title = '<b>Gapminder</b><br>2007 Average GDP Per Cap & Life Exp. by Continent',
    yaxis = dict(
        type = 'log'
    ),
    images=[dict(
            source=encoded_image,
            xref="paper", yref="paper",
            x=1.1, y=-0.1,
            sizex=0.5, sizey=0.75,
            sizing='stretch',
            opacity=0.5,
            xanchor="right", yanchor="bottom"
        )],
)


plot({'data': data, 'layout': layout}, validate=False)
