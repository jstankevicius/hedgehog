import sqlite3
import time
import os
import hedgehog.core.keys as keys

from datetime import datetime
from alpha_vantage.timeseries import TimeSeries

# Helper functions:
def pandas_to_list(index, row):
    """Reformats pandas-format data from AV into a list."""

    timedata = str(index).split()
    price_list = [row["1. open"], row["2. high"], row["3. low"], row["4. close"], row["5. volume"]]

    # A list in the form [YYYY, MM, DD]; all entries are integers.
    date_list = [int(s) for s in timedata[0].split("-")]
    result = []

    # If we have 2 elements, then there is both a date and a time string.
    if len(timedata) == 2:

        # In this case, timedata[1] is the time string in the form HH:MM:SS.
        # Seconds will always be 0, so we don't have to worry about them.
        time_list = timedata[1].split(":")[:2]
        result = date_list + time_list + price_list
    else:
        result = date_list + price_list
    
    return result


# In the future, I can probably just import a list from somewhere.
def get_symbols():
    """Returns all stock symbols in data//symbols.txt as a list."""

    with open("data//symbols.txt", "r") as symbol_file:
        symbol_list = [symbol.rstrip() for symbol in symbol_file.readlines()]
        return symbol_list


class DataManager:
    """Class to help maintain a database of intraday/daily stock data."""

    def __init__(self, db_path, schema_path=None):
        """Connects the DataManager object to a database. If the database file does not
        exist, it creates the file. If a schema_path argument is provided (as a string),
        connect() executes the schema."""

        # Time series object we use to fetch data from AV:
        self.time_series = TimeSeries(keys.AV_KEY, output_format="pandas")

        # Where we store all the changes that would be written to the database:
        self.changes = []

        # Last time the file was modified:
        # It seems like bad practice to initialize variables as NoneType...
        self.last_modified = None
        statbuf = None

        try:
            statbuf = os.stat(db_path)

        except FileNotFoundError:
            print(db_path, "does not exist, creating file")

            # Is this a hacky way of creating the file?
            with open(db_path, "w"):
                pass

        self.last_modified = datetime.fromtimestamp(statbuf.st_mtime)
        self.connection = sqlite3.connect(db_path)


        # execute schema:
        if schema_path is not None:
            with open(schema_path) as schema:
                self.connection.executescript(schema.read())


    def get_changes(self):
        """Returns all new fetched rows as an array."""
        return self.changes

    # This seems like terrible design...
    def get_connection(self):
        """Returns the object's connection as an object."""
        return self.connection


    # This function doesn't feel "clean." I suppose that's fine, since this entire 
    # class is basically just a glorified script, but using strings as arguments
    # and returning variable-length lists of data seems sketchy. Maybe I'll figure
    # something out in the future.
    def fetch(self, period, symbols=[], verbose=False):
        """Fetches data from the given time period over the given set of symbols. 
        fetch() then determines the relevant new data  and appends it to self.changes."""

        print("Database last modified at {}".format(self.last_modified))
        print("Symbol\tFirst\t\t\tMost Recent\t\tChanges")

        errors = 0

        for stock_symbol in symbols:

            data = None

            try:

                if period == "intraday":
                    data = self.time_series.get_intraday(symbol=stock_symbol, outputsize="full", interval="5min")[0]

                elif period == "daily":
                    data = self.time_series.get_daily(symbol=stock_symbol, outputsize="full")[0]

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

                row_time = datetime(*data_list[:3])

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
