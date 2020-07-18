import sqlite3
import time
import os
import hedgehog.config as config

from datetime import datetime
from alpha_vantage.timeseries import TimeSeries


SYMBOLS = (
    
    "FB", "AAPL", "AMZN", "NFLX", "GOOG", "TSLA", "SHOP", "NVDA", "SPOT", "MSFT", "AMD", "SQ", 
    "ROKU", "DAL", "AAL", "UAL", "JPM", "NCLH", "CCL", "BAC", "ABBV", "GILD", "XOM", "PSX", "ZM",
    "BABA", "JNJ", "WMT", "HD", "PFE", "DIS", "MRK", "NKE", "MCD", "COST", "GSK", "CVS", "BA", 
    "BKNG", "CAT", "UBER", "MU", "WBA", "WDAY", "LULU", "CMG", "TWTR", "PANW", "LUV", "MDB"
)

class QueryObject():
    pass


class DataManager:
    """
    
    Provides an interface for interacting with the database files. 
    
    Supports fetching data from AlphaVantage (the data provider), writing it to the database and 
    querying the database in pure SQLite.
    
    Example usage:
    -----------------------
    >>> import hedgehog.database as db
    >>> from pprint import pprint
    >>> m = db.DataManager("data//databases//daily.db")
    >>> results = m.query_db("SELECT * FROM prices WHERE symbol=? ORDER BY time", ("MSFT",))
    >>> pprint(results)
    ('MSFT', 1591074000.0, 184.25, 185.0, 181.35, 184.91, 30794585),
    ('MSFT', 1591160400.0, 184.815, 185.94, 183.58, 185.36, 27311016),
    ('MSFT', 1591246800.0, 184.3, 185.84, 182.3, 182.92, 28659255),
    ('MSFT', 1591333200.0, 182.62, 187.73, 182.01, 187.2, 39778315)

    """

    def __init__(self, db_path, schema_path=None):
        """
        Connects the DataManager object to a database. If the database file does not exist, it 
        creates the file. If a schema_path argument is provided (as a string), the connection object 
        executes the schema.
        """

        self.time_series = TimeSeries(config.AV_KEY, output_format="pandas")
        self.changes = []
        self.connection = sqlite3.connect(db_path)

        # execute schema:
        if schema_path is not None:
            with open(schema_path) as schema:
                self.connection.executescript(schema.read())


    def get_changes(self):
        """Returns all new fetched rows as an array."""
        return self.changes


    def parse_changes_from_df(self, symbol, data_frame):
        """
        Parses a symbol DataFrame and appends rows that are not yet in the database to self.changes.
        """

        new_rows = 0

        # Grab the row from last_unix_time where the symbol matches. There should only be one row
        # per symbol. The second element is the UTC time at which the symbol was last modified. If
        # an empty tuple is returned, we treat last modified date as UTC time 0.
        row = self.query_db("SELECT * FROM last_updated WHERE symbol=?", (symbol,), one=True)
        last_unix_time = row[1] if row else 0

        for index, row in data_frame.iterrows():

            row_unix_time = datetime.strptime(str(index), "%Y-%m-%d %H:%M:%S").timestamp()
            data_list = [row_unix_time] + list(row)

            if row_unix_time > last_unix_time:
                self.changes.append([symbol] + data_list)
                new_rows += 1

        # There are cases where we could be parsing 0 rows. In that case, we will be making no new
        # additions to the symbol's prices, so the entry in last_updated should not be modified.
        # If this is a new symbol, we'll need to use INSERT INTO. If this symbol already exists
        # in the table, we'll need to use UPDATE.
        if len(data_frame) > 0:
            cur_time = time.time()

            if last_unix_time == 0:
                self.query_db("INSERT INTO last_updated VALUES (?, ?)", (symbol, cur_time))
            
            else:
                self.query_db("UPDATE last_updated SET time = ? WHERE symbol = ?", (cur_time, symbol))

        return new_rows


    def get_prices(self, symbols, period, verbose=False):
        """
        For all provided symbols, fetches data from AlphaVantage (assumed Standard API), parses
        each symbol's historic prices, and appends to self.changes the rows for every symbol that
        have not yet been written to the database.
        """

        TIMEOUT = 0 if len(symbols) == 1 else 13

        if verbose:
            print("Symbol\tLast refreshed\tFetched rows\tNew rows")

        for stock_symbol in symbols:
            data_frame = None
            metadata = None

            try:
                
                if period == "intraday":
                    data_frame, metadata = self.time_series.get_intraday(symbol=stock_symbol, interval="5min", outputsize="full")

                elif period == "daily":
                    data_frame, metadata = self.time_series.get_daily_adjusted(symbol=stock_symbol, outputsize="full")

                else:
                    raise Exception("Invalid period. Provide either 'intraday' or 'daily'.")
            
            except ValueError as e:
                print(stock_symbol, e)
                continue

            new_rows = self.parse_changes_from_df(stock_symbol, data_frame)

            if verbose:
                print("{}\t{}\t{}\t\t{}".format(stock_symbol, metadata["3. Last Refreshed"], len(data_frame), new_rows))

            time.sleep(TIMEOUT)


    def query_db(self, query, args=(), one=False):
        """
        Executes the given query with the provided arguments and returns the results (if any are 
        required). If 'one' is set to True, returns only the first result (or an empty tuple).
        """

        cur = self.connection.execute(query, args)
        query_list = cur.fetchall()

        cur.close()
        self.connection.commit()

        return (query_list[0] if query_list else ()) if one else query_list


    # TODO: find some other way to do this. We should make an analogue to executemany().
    def commit_changes(self):
        """
        Inserts all rows in self.changes into the database.
        """

        # Preset number of columns. Bad practice? Probably.
        self.connection.executemany("INSERT INTO prices VALUES (?,?,?,?,?,?,?,?,?,?)", self.changes)
        self.connection.commit()
