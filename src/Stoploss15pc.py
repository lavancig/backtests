from backtesting import Backtest
from backtesting.lib import crossover, TrailingStrategy
from backtesting.test import SMA, GOOG
import yfinance as yf
from datetime import datetime, timedelta
dayOfMonth = 28

epoch = datetime(1971, 1, 1, 0, 0, 0)

class SMA200Monthly(TrailingStrategy):
    def init(self):
        super().init()
        super().set_trailing_sl(5)
        self.price = self.data.Close

        self.oldPrice = 0
        self.lastPos = epoch
        self.sma = self.I(SMA, self.price, 200)


    def next(self):
        super().next()
        day = int(datetime.strftime(self.data.index[-1], '%d'))
        oneDayBefore = int(datetime.strftime(self.data.index[-2], '%d'))

        dayToTrade = (day == dayOfMonth) or (((oneDayBefore < dayOfMonth)  and (day > dayOfMonth)) 
                                             or ((oneDayBefore < dayOfMonth) and (oneDayBefore > 20) and (day < 5)))

        price = self.data.Close[-1]
        timeNow = datetime.strptime(self.data.index[-1]._date_repr, '%Y-%m-%d')
        if self.position.size <= 0 and timeNow - self.lastPos >= timedelta(days=90) and price > self.sma[-1]:
            self.buy(sl=0.85 * price)
            self.oldPrice = price
        elif price > self.oldPrice and self.position.size > 0:
            self.oldPrice = price
            super().trades[0].sl = 0.85 * price

        if self.position.size > 0:
            self.lastPos = timeNow



start = datetime(2010, 1, 1)
end = datetime(2024, 8, 22)

        # yf.Isin()
data =  yf.download("URTH", start=start, end=end)
bcktest = Backtest(data, SMA200Monthly, commission=0, exclusive_orders=True)
stats = bcktest.run()

print(stats)
bcktest.plot()