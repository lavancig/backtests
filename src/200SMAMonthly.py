from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import yfinance as yf
from datetime import datetime
dayOfMonth = 28

class SMA200Monthly(Strategy):
    def init(self):
        super().init()
        self.price = self.data.Close
        self.sma = self.I(SMA, self.price, 200)
        self.sma2 = self.I(SMA, self.price, 50)

    def next(self):
        day = int(datetime.strftime(self.data.index[-1], '%d'))
        oneDayBefore = int(datetime.strftime(self.data.index[-2], '%d'))

        dayToTrade = (day == dayOfMonth) or (((oneDayBefore < dayOfMonth)  and (day > dayOfMonth)) 
                                             or ((oneDayBefore < dayOfMonth) and (oneDayBefore > 20) and (day < 5)))

        price = self.data.Close[-1]
        # self.position.size
        # print(self.data)
        if dayToTrade and price > self.sma[-1] and self.position.size <= 0:
        # if crossover(self.sma2, self.sma):
            self.buy()
            # self.sell()
        elif dayToTrade and price < self.sma[-1] and self.position.size > 0:
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