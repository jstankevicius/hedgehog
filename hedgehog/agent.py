import hedgehog.database as db
import numpy as np
import pandas as pd
import math
from pprint import pprint

class Agent:

    def __init__(self):
        self.universe = None

    def act(self):
        """If today's price is higher than yesterday's , we buy 50. If it's lower by a 
        dollar, we sell everything we have. Otherwise, we do nothing."""

        history = self.universe.get_history()
        today = history.iloc[-1]
        yesterday = history.iloc[-2]

        prev = yesterday['Close']
        curr = today['Close']
        
        if curr > prev  and self.universe.get_capital() >  curr*50:
            self.universe.buy("TSLA", 50)
            print(self.universe.cur_date(), "Bought at", curr)

        elif curr < prev *0.01 and self.universe.get_portfolio()["TSLA"] > 0:

            # Dump entire portfolio
            self.universe.sell("TSLA", self.universe.get_portfolio()["TSLA"])
            print(self.universe.cur_date(), "Sold at", today["Close"])

        else:
            print(self.universe.cur_date(), "Did nothing")
            pass

    def link_universe(self, universe):
        self.universe = universe
