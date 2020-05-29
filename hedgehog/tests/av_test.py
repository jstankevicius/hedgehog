import core
import unittest
from alpha_vantage.timeseries import TimeSeries


# This is just here so I don't forget the format of intraday
# vs daily data.

class TestAVDataFetch(unittest.TestCase):

    def test(self):
        ts = TimeSeries(core.keys.AV_KEY, output_format="pandas")
        ts.get_daily(symbol="MSFT", outputsize="compact")
        ts.get_intraday(symbol="MSFT", interval="5min", outputsize="compact")[0]
        self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()