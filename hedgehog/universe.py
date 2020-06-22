"""
Maybe something like this?

agent = Agent()
uni = BacktestUniverse()

# Link agent and universe together
agent.link_universe(uni)

# Set time to beginning of universe
agent.start() 

# Run until there is no more data
while not uni.end()
    agent.act()
    uni.next_state()

in Agent:
def act(self):
    history = self.universe.history().tail(2)

    if history[-1] > history[-2]:
        self.universe.buy()

"""
import hedgehog.database as db
import pandas as pd

from datetime import datetime

class Universe:

    def __init__(self):

        # A Pandas dataframe.
        self.history = None

    def buy(self, symbol, shares):
        """
        Abstracts away the idea of 'buying' some number of shares for a particular symbol. If the
        buy is successful (the order is filled), the corresponding number of shares are placed into
        the agent's portfolio, and the investment is subtracted from capital.
        """

        pass

    def sell(self, symbol, shares):
        """
        Abstracts away the idea of 'selling' some number of shares for a particular symbol. If the
        sell is successful (the order is filled), the profits are deposited into the agent's
        capital, and the corresponding number of shares are removed from the portfolio.
        """

        pass

    def next_state(self):

        """
        Abstracts the passage of time, either real or artificial, by loading the 'next' set of
        prices into the internal state of the universe. In backtesting, this is equivalent to just
        advancing to the next row of prices. In real life, this might include waiting 60 seconds 
        or even a full day until the next set of prices arrives.
        """

        pass

    def cur_state(self):
        pass


class BacktestUniverse(Universe):
    
    def __init__(self):
        m = db.DataManager("data//databases//daily.db")
        self.cur_index = 0
        self.capital = 100000
        self.portfolio = {"MSFT": 0}

        results = m.query_db("SELECT open, high, low, close, volume FROM prices WHERE symbol=? ORDER BY time", ("MSFT",))
        time_idx = [datetime.fromtimestamp(n[0]) for n in m.query_db("SELECT TIME FROM prices WHERE symbol=? ORDER BY time", ("MSFT",))]
        
        self.history = pd.DataFrame(results, index=time_idx, columns=["Open", "High", "Low", "Close", "Volume"])
    
    def get_capital(self):
        return self.capital

    def get_portfolio(self):
        return self.portfolio

    def next_state(self):
        self.cur_index += 1

    def get_history(self):
        return self.history.iloc[:self.cur_index]

    def cur_state(self):
        return self.history.iloc[self.cur_index]

    def buy(self, symbol, shares):
        assert self.capital >= self.cur_state()["Close"]*shares

        self.capital -= self.cur_state()["Close"]*shares
        self.portfolio[symbol] += shares

    def cur_date(self):
        return self.history.index.values[self.cur_index]

    def sell(self, symbol, shares):
        assert self.portfolio[symbol] > 0

        self.capital += self.cur_state()["Close"]*shares
        self.portfolio[symbol] -= shares
