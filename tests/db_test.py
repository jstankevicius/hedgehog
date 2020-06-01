import hedgehog.config as config
import hedgehog.database as db
import unittest
from alpha_vantage.timeseries import TimeSeries


# This is just here so I don't forget the format of intraday
# vs daily data.

class TestDatabase(unittest.TestCase):

    def test_av_access(self):

        try:
            ts = TimeSeries(config.AV_KEY, output_format="pandas")
            ts.get_daily(symbol="MSFT", outputsize="compact")
            ts.get_intraday(symbol="MSFT", interval="5min", outputsize="compact")[0]
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_data_loader(self):
        pass

if __name__ == "__main__":
    unittest.main()