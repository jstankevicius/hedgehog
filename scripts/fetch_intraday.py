import hedgehog.database as db

manager = db.DataManager("data/databases/intraday.db", "data/schema/price_schema.sql")
manager.get_prices(db.SYMBOLS, "intraday", verbose=True)
manager.commit_changes()