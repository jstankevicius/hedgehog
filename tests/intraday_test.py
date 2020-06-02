import unittest
import hedgehog.database as db


class TestDataManager(unittest.TestCase):

    def test_fetch(self):
        manager = db.DataManager("intraday.db", "data//schema//price_schema.sql")
        manager.get_prices(["MSFT"], "intraday")

if __name__ == "__main__":
    unittest.main()