#!usr/bin/env python3
import hedgehog.database as db

manager = db.DataManager("data/databases/daily.db", "data/schema/intraday_schema.sql")
manager.fetch_daily(symbols=["MSFT"], verbose=True)

conn = manager.get_connection()
conn.executemany("INSERT INTO PRICES VALUES(?,?,?,?,?,?,?,?,?,?,?)", manager.get_changes())
conn.commit()
