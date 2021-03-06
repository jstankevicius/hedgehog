import hedgehog.database as db

manager = db.DataManager("data/databases/daily_adjusted.db", 'data/schema/price_schema.sql')
manager.get_prices(db.SYMBOLS, "daily", verbose=True)
manager.commit_changes()