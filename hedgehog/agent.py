import hedgehog.database as db
import numpy as np
import pandas as pd
import math
from pprint import pprint

class Agent:

    def __init__(self):
        self.universe = None

    def act(self):

        history = self.universe.get_history()
        today = history.iloc[-1]
        yesterday = history.iloc[-2]

        prev = yesterday['Close']
        curr = today['Close']
        
        if curr < prev *0.99  and self.universe.get_capital() >  curr*50:
            poss_shares = int(self.universe.get_capital() // curr)
            print(poss_shares)
            print(prev)
            self.universe.buy("AAPL", poss_shares)
            print(self.universe.cur_date(), "Bought at", curr)

        elif curr > prev *1.01 and self.universe.get_portfolio()["AAPL"] > 0:

            # Dump entire portfolio
            self.universe.sell("AAPL", self.universe.get_portfolio()["AAPL"])
            print(self.universe.cur_date(), "Sold at", today["Close"])

        else:
            print(self.universe.cur_date(), "Did nothing")
            pass

    def link_universe(self, universe):
        self.universe = universe
