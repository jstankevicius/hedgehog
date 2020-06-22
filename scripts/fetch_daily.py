import hedgehog.database as db

manager = db.DataManager("data/databases/daily.db")
manager.get_prices(db.SYMBOLS, "daily", verbose=True)
manager.commit_changes()