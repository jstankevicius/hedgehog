import hedgehog.database as db
import numpy as np
import pandas as pd

from pprint import pprint
from hedgehog.agent import Agent
from datetime import datetime

from hedgehog.universe import BacktestUniverse 

b = BacktestUniverse()
a = Agent()
a.link_universe(b)

print("Start:", b.get_capital())
b.next_state()
b.next_state()

for i in range(4000):
    a.act()
    b.next_state()


print("End:", b.get_capital() + b.get_portfolio()["MSFT"]*b.cur_state()["Close"])