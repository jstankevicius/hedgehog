import unittest
import hedgehog.core.database as db


class TestDataManager(unittest.TestCase):

    def test_fetch(self):
        manager = db.DataManager("intraday.db")
        manager.fetch("intraday", symbols=["MSFT"])

if __name__ == "__main__":
    unittest.main()