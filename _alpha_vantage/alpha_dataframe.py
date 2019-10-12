import pandas as pd
from alpha_vantage.techindicators import  TechIndicators
from alpha_vantage.timeseries import TimeSeries
from _alpha_vantage.key import api_key
import datetime

stock = input('What stock do you want?')
print('')

api_key = api_key
def rsi_dataframe(stock=stock):

    period = 60
    ts = TimeSeries(key=api_key, output_format='pandas')
    data_ts = ts.get_intraday(stock.upper(), interval='1min', outputsize='full')

    ti = TechIndicators(key=stock.upper(), output_format='pandas')

    data_ti, meta_data_ti = ti.get_bbands(symbol=stock.upper(), interval='1min', time_period=period, series_type='close')


    df = data_ts[0][period::]

    # df.index = pd.Index(map(lambda x: str(x)[:-3], df.index))

    df2 = data_ti


    total_df = pd.merge(df,  df2, on="date")

    low = []
    for l in total_df['3. low']:
        low.append(float(l))

    high = []
    for h in total_df['2. high']:
        high.append(float(h))

    bb_low = []
    for bl in total_df['Real Lower Band']:
        bb_low.append(float(bl))

    bb_high = []
    for bh in total_df['Real Upper Band']:
        bb_high.append(float(bh))


    buy = []
    buy_index = []

    for bl, p, i in zip(bb_low, low, total_df.index[::-1]):
        if p < bl:
            if not buy_index:
                buy.append(p)
                buy_index.append(i)
            else:
                index_need_to_beat = buy_index[-1] + datetime.timedelta(minutes=30)
                if i > index_need_to_beat:
                    buy.append(p)
                    buy_index.append(i)

    # If Price signals a good sell

    sell = []
    sell_index = []
    for bh, p, i in zip(bb_high, high, total_df.index[::-1]):
        if p < bh:
            if not sell_index:
                sell.append(p)
                sell_index.append(i)
            else:
                index_need_to_beat = sell_index[-1] + datetime.timedelta(minutes=30)
                if i > index_need_to_beat:
                    sell.append(p)
                    sell_index.append(i)

    buy_positions = 0
    profit = 0
    stocks = 0
    buy_point = 0
    sell_point = 0

    while buy_point != len(buy):
        if buy_index[buy_point] < sell_index[sell_point]:
            buy_positions += round(float(buy[buy_point]))
            print(f'buy position = {buy[buy_point]} total positions = {round(buy_positions, 2)} at sell index = {sell_index[sell_point]}')
            buy_point += 1
            stocks += 1
        else:
            print(f'sold at {sell[sell_point]}')
            profit += buy_positions - (float(sell[sell_point]) * stocks)
            profit = round(profit, 2)
            print(f'profit = {profit}')
            print('')
            buy_positions = 0
            stocks =0
            sell_point += 1
    else:
        pass

    # for h in total_df.head():
    #     print(h)
    return print(f'${profit}')
rsi_dataframe()