import unittest
import hedgehog.database as db


class TestDataManager(unittest.TestCase):

    def test_fetch(self):
        manager = db.DataManager("intraday.db")
        manager.fetch_daily(symbols=["MSFT"])

if __name__ == "__main__":
    unittest.main()