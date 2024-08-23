from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
from datetime import datetime
import pandas as pd
import talib
dayOfMonth = 28

def EMA_Backtesting(values, n):
    """
    Return exponential moving average of `values`, at
    each step taking into account `n` previous values.
    """
    close = pd.Series(values)
    return talib.EMA(close, timeperiod=n)

class SMA200Monthly(Strategy):
    def init(self):
        super().init()
        self.price = self.data.Close
        self.ema20 = self.I(EMA_Backtesting, self.price, 140)
        self.ema10 = self.I(EMA_Backtesting, self.price, 70)

    def next(self):
        day = int(datetime.strftime(self.data.index[-1], '%d'))
        oneDayBefore = int(datetime.strftime(self.data.index[-2], '%d'))

        dayToTrade = (day == dayOfMonth) or (((oneDayBefore < dayOfMonth)  and (day > dayOfMonth)) 
                                             or ((oneDayBefore < dayOfMonth) and (oneDayBefore > 20) and (day < 5)))

        price = self.data.Close[-1]
        # self.position.size
        # print(self.data)
        # if dayToTrade and price > self.sma[-1] and self.position.size <= 0:
        if crossover(self.ema10, self.ema20):
            self.buy()
            # self.sell()
        if crossover(self.ema20, self.ema10):
        # elif price < self.sma[-1] and self.position.size > 0:
        # if crossover(self.sma, self.sma2):
            self.position.close()


start = datetime(2010, 1, 1)
end = datetime(2024, 8, 22)

        # yf.Isin()
data =  yf.download("URTH", start=start, end=end)
bcktest = Backtest(data, SMA200Monthly, commission=0, exclusive_orders=True)
stats = bcktest.run()

print(stats)
bcktest.plot()