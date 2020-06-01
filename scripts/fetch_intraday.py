import hedgehog.database as db

manager = db.DataManager("data/databases/intraday.db", "data/schema/price_schema.sql")
manager.fetch_intraday(symbols=["MSFT"], verbose=True)

conn = manager.get_connection()
conn.executemany("INSERT INTO PRICES VALUES(?,?,?,?,?,?,?,?,?,?,?)", manager.get_changes())
conn.commit()
