from database import DataManager

d = DataManager()
d.connect("data//intraday.db")
d.fetch()
d.commit()