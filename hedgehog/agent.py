import hedgehog.database as db
import numpy as np
import pandas as pd
import math
from pprint import pprint

class Agent:

    def __init__(self):
        self.universe = None

    def act(self):
        """If today's price is higher than yesterday's by a dollar, we buy 50. If it's lower by a 
        dollar, we sell everything we have. Otherwise, we do nothing."""

        history = self.universe.get_history()
        today = history.iloc[-1]
        yesterday = history.iloc[-2]
        
        if today["Close"] > yesterday["Close"] and self.universe.get_capital() > today["Close"]*50:
            self.universe.buy("MSFT", 50)
            print(self.universe.cur_date(), "Bought at", today["Close"])

        elif today["Close"] < yesterday["Close"] and self.universe.get_portfolio()["MSFT"] > 0:

            # Dump entire portfolio
            self.universe.sell("MSFT", self.universe.get_portfolio()["MSFT"])
            print(self.universe.cur_date(), "Sold at", today["Close"])

        else:
            print(self.universe.cur_date(), "Did nothing")
            pass

    def link_universe(self, universe):
        self.universe = universe
