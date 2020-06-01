import sqlite3
import time
import os
import hedgehog.config as config

from datetime import datetime
from alpha_vantage.timeseries import TimeSeries


def index_to_datetime_ints(index):
    """Given some string representing a datetime in the form YYYY-MM-DD HH:MM:SS,
    returns the year, month, day, hour, minute as a list of integers. AlphaVantage
    does not allow intra-minute data, so the seconds will always be 00. Hence, the
    seconds place is discarded."""
    date_string, time_string = str(index).split()
    date_int_list = [int(n) for n in date_string.split("-")]
    time_int_list = [int(n) for n in time_string.split(":")]

    return date_int_list + time_int_list


# In the future, I can probably just import a list from somewhere.
def get_symbols():
    """Returns all stock symbols in data//symbols.txt as a list."""

    with open("data//symbols.txt", "r") as symbol_file:
        symbol_list = [symbol.rstrip() for symbol in symbol_file.readlines()]
        return symbol_list


class DataManager:

    def __init__(self, db_path, schema_path=None):
        """Connects the DataManager object to a database. If the database file does not
        exist, it creates the file. If a schema_path argument is provided (as a string),
        connect() executes the schema."""

        self.time_series = TimeSeries(config.AV_KEY, output_format="pandas")
        self.changes = []
        self.last_modified = datetime.fromtimestamp(0)

        try:
            statbuf = os.stat(db_path)
            self.last_modified = datetime.fromtimestamp(statbuf.st_mtime)

        except FileNotFoundError:
            print(db_path, "does not exist, sqlite3.connect() will create file...")
        
        self.connection = sqlite3.connect(db_path)


        # execute schema:
        if schema_path is not None:
            with open(schema_path) as schema:
                self.connection.executescript(schema.read())


    def get_changes(self):
        """Returns all new fetched rows as an array."""
        return self.changes

    # Is directly returning the connection object bad practice? Probably.
    def get_connection(self):
        """Returns the object's connection as an object."""
        return self.connection


    def parse_dataframe(self, symbol, data):
        new_rows = 0

        for index, row in data.iterrows():

            # Intraday datapoints contain both the date and time
            data_list = index_to_datetime_ints(index) + list(row)
            row_datetime = datetime(*data_list[:5])

            if row_datetime > self.last_modified:
                self.changes.append([symbol] + data_list)
                new_rows += 1

        return new_rows


    def fetch_intraday(self, symbols=[], verbose=False):
        TIMEOUT = 0 if len(symbols) == 1 else 13

        if verbose:
            print("Database last modified at {}".format(self.last_modified))
            print("Symbol\tLast refreshed\tFetched rows\tNew rows")

        for stock_symbol in symbols:
            data = None
            metadata = None

            try:
                data, metadata = self.time_series.get_intraday(symbol=stock_symbol, interval="5min", outputsize="full")
            
            except ValueError as e:
                print(stock_symbol, e)
                continue

            new_rows = self.parse_dataframe(stock_symbol, data)

            if verbose:
                print("{}\t{}\t{}\t\t{}".format(stock_symbol, 
                                                metadata["3. Last Refreshed"], 
                                                len(data), 
                                                new_rows))

            time.sleep(TIMEOUT)


    def fetch_daily(self, symbols=[], verbose=False):
        TIMEOUT = 0 if len(symbols) == 1 else 13

        if verbose:
            print("Database last modified at {}".format(self.last_modified))
            print("Symbol\tLast refreshed\tFetched rows\tNew rows")

        for stock_symbol in symbols:
            data = None
            metadata = None

            try:
                data, metadata = self.time_series.get_daily(symbol=stock_symbol, outputsize="full")
            
            except ValueError as e:
                print(stock_symbol, e)
                continue

            new_rows = self.parse_dataframe(stock_symbol, data)

            if verbose:
                print("{}\t{}\t{}\t\t{}".format(stock_symbol, 
                                                metadata["3. Last Refreshed"], 
                                                len(data), 
                                                new_rows))

            time.sleep(TIMEOUT)
