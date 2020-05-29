import sqlite3
import time
import os
import core.keys as keys

from datetime import datetime
from enum import Enum
from alpha_vantage.timeseries import TimeSeries

# Helper functions:
def pandas_to_list(index, row):
    """Reformats pandas-format data from AV into a list."""

    timedata = str(index).split()

    # Format: yyyy-mm-dd
    date = timedata[0]
    timeofday = timedata[1]

    return [date,
            timeofday,
            row["1. open"],
            row["2. high"],
            row["3. low"],
            row["4. close"],
            row["5. volume"]]


def get_symbols():
    """Returns all stock symbols in data//symbols.txt as a list."""

    with open("data//symbols.txt", "r") as symbol_file:
        symbol_list = [symbol.rstrip() for symbol in symbol_file.readlines()]
        return symbol_list

class DataManager:
    """Class to help maintain a database of intraday stock data."""

    def __init__(self):
        self.last_modified = None
        self.time_series = TimeSeries(keys.AV_KEY, output_format="pandas")

        # Where we store all the changes that would be written to the database.
        self.changes = []

        # If we try to call get_intraday on a symbol that is no longer listed on the
        # market, AlphaVantage will raise a ValueError instead of telling us that it
        # can't find that symbol. It might be useful to store such symbols here during
        # init_write() and fetch(), and then clear them from our database using some
        # other function.
        self.missing = []
        self.connection = None


    # I could probably combine connect and init_db into __init__. Maybe.
    def connect(self, db_path):
        """Connects the DataLoader object to a database."""
        statbuf = os.stat(db_path)

        # datetime object:
        self.last_modified = datetime.fromtimestamp(statbuf.st_mtime)
        self.connection = sqlite3.connect(db_path)


    def init_db(self, db_path, schema_path):
        """Given a path to a database file (regardless of whether the file exists or
        not), connects to the database and executes the schema file."""
        self.connect(db_path)

        with open(schema_path) as schema:
            self.connection.executescript(schema.read())


    def fetch(self, period, symbols=get_symbols()):
        """Fetches data from the given time period over the given set of symbols. 
        fetch() then determines the relevant new data  and appends it to self.changes."""

        print("Database last modified at {}".format(self.last_modified))
        print("Symbol\tFirst\t\t\tMost Recent\t\tChanges")

        errors = 0

        for stock_symbol in symbols:

            data = None

            try:

                if period == "intraday":
                    data = self.time_series.get_intraday(symbol=stock_symbol,
                                                         outputsize="full",
                                                         interval="5min")[0]
                elif period == "daily":
                    data = self.time_series.get_daily(symbol=stock_symbol,
                                                      outputsize="full")[0]

            except ValueError as error:
                print(stock_symbol + ": " + str(error))
                errors += 1

                # TODO: handle cases where there is no symbol vs when AV tells us to slow down
                continue

            # How many new rows were added to the database for this symbol:
            deltas = 0

            # The most recent row entry:
            most_recent = data.first_valid_index()

            for index, row in data.iterrows():
                data_list = pandas_to_list(index, row)

                # string in the form of "2020-05-19 13:57:00"
                datetime_string = " ".join((data_list[0], data_list[1])) 

                # the actual datetime object
                row_time = datetime.strptime(datetime_string, "%Y-%m-%d %H:%M:%S")

                # If this is new data, we append it to self.changes.
                if row_time > self.last_modified:
                    self.changes.append([stock_symbol] + data_list)
                    deltas += 1

            # The last row in the dataframe is actually the row corresponding to the date
            # the furthest away from today. So the last row in "changes" is actually the
            # first row by date that we inserted.
            last_modified = " ".join((self.changes[-1][1:3]))
            print("{}\t{}\t{}\t{}".format(stock_symbol, last_modified, most_recent, deltas))

            # Hardcoded wait time to avoid AV throttling.
            # Apparently now you can't make calls as frequently as before :( Standard API
            # rate is 5 calls per minute.
            time.sleep(13)

        print("Fetched {} new datapoints with {} errors.".format(len(self.changes), errors))


    def commit(self):
        """Commits the changes in self.changes to the database."""

        if self.connection is None:
            raise Exception("No database connected to DataManager. Use connect(db_path).")
        
        # The intraday database will have different columns... uGH
        self.connection.executemany("INSERT INTO prices VALUES (?,?,?,?,?,?,?,?)", self.changes)
        self.connection.commit()
