import numpy as np
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.offline as pyo
pyo.init_notebook_mode()
from feeds import PandasData

import requests

import talib

symbols = ['PRIO3']

initial_date = "2023-01-01T00:00:00.000Z"
final_date = "2023-10-20T23:59:59.999Z"

dfs = {}
for symbol in symbols:
    url = f"http://DESKTOP-3V2V0BR.local:8000/prices?symbol={symbol}&timeframe=TIMEFRAME_D1&initial_date={initial_date}&final_date={final_date}"
    r = requests.get(url)
    if r.status_code != 200:
        raise Exception(f"Error to get prices of {symbol} symbol")

    json_data = r.json()
    df = pd.DataFrame(json_data)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index("timestamp")


    df['sma_close_5'] = talib.SMA(df.close, 5)
    df['sma_close_10'] = talib.SMA(df.close, 10)
    df['sma_close_20'] = talib.SMA(df.close, 20)

    dfs[symbol] = df


df = dfs[symbols[0]]
df = df.rename(columns={"real_volume": "volume"}, errors="raise")

print(df.head())
df['openinterest'] = 0

from datetime import datetime
import backtrader as bt

data = PandasData(dataname=df, datetime='datetime', nocase=True)

class SmaCross(bt.SignalStrategy):
    def __init__(self):
        sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
        crossover = bt.ind.CrossOver(sma1, sma2)
        self.signal_add(bt.SIGNAL_LONG, crossover)


cerebro = bt.Cerebro()
cerebro.adddata(data)
cerebro.addstrategy(SmaCross)


cerebro.run()
cerebro.plot(volume=False)
