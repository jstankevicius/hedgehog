import hedgehog.database as db
from pprint import pprint

m = db.DataManager("data//databases//daily.db")

results = m.query_db("SELECT * FROM prices WHERE symbol=? ORDER BY year, month, day", ("MSFT",))
pprint(results)


