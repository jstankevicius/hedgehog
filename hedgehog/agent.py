import hedgehog.database as db
import numpy as np
import pandas as pd
from pprint import pprint

class Agent:

    def __init__(self):
        self.universe = None

    def act(self):
        """If today's price is higher than yesterday's by a dollar, we buy 50. If it's lower by a 
        dollar, we sell everything we have. Otherwise, we do nothing."""

        history = self.universe.get_history()
        idx = history.iloc 
        
        if round(idx[-1]["Close"]) > round(idx[-2]["Close"]) and self.universe.get_capital() > idx[-1]["Close"]*50:
            self.universe.buy("MSFT", 50)
            print("Bought at", idx[-1]["Close"])

        elif round(idx[-1]["Close"]) < round(idx[-2]["Close"]) and self.universe.get_portfolio()["MSFT"] > 0:

            # Dump entire portfolio
            self.universe.sell("MSFT", self.universe.get_portfolio()["MSFT"])
            print("Sold at", idx[-1]["Close"])

        else:
            print("Did nothing")
            pass

    def link_universe(self, universe):
        self.universe = universe
