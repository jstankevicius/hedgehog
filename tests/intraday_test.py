import unittest
import hedgehog.database as db


class TestDataManager(unittest.TestCase):

    def test_fetch(self):
        manager = db.DataManager("tests//tmp//intraday.db", "data//schema//price_schema.sql")
        manager.get_prices(["MSFT"], "daily")
        manager.commit_changes()
        results = manager.query_db("SELECT * FROM prices WHERE symbol=? ORDER BY time", ("MSFT",))
        self.assertGreater(len(results), 0)

if __name__ == "__main__":
    unittest.main()