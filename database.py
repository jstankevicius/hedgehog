import sqlite3
import time
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

    with open("symbols.txt", "r") as symbol_file:
        symbol_list = [symbol.rstrip() for symbol in symbol_file.readlines()]
        return symbol_list

class DataManager:
    """Class to help maintain a database of intraday stock data."""

    def __init__(self):
        self.last_modified = None
        self.time_series = TimeSeries("J4XLT1RK0S2QK5X0", output_format="pandas")
        self.symbols = get_symbols()

        # Where we store all the changes that would be written to the database.
        self.changes = []

        # If we try to call get_intraday on a symbol that is no longer listed on the
        # market, AlphaVantage will raise a ValueError instead of telling us that it
        # can't find that symbol. It might be useful to store such symbols here during
        # init_write() and fetch(), and then clear them from our database using some
        # other function.
        self.missing = []
        self.connection = None


    def connect(self, db_path):
        """Connects the DataLoader object to a database."""
        #statbuf = os.stat(db_path)
        #self.last_modified = statbuf.st_mtime
        self.connection = sqlite3.connect(db_path)


    def init_db(self, db_path, schema_path):
        """Creates the initial database file and sets up the schema."""
        self.connect(db_path)

        with open(schema_path) as schema:
            self.connection.executescript(schema.read())

    def fetch(self):
        """Fetches most recent intraday data for every symbol."""
        # TODO: provide enum argument so we can fetch for one, a set, or all symbols.

        for stock_symbol in self.symbols:
            print("Fetching data for {}...".format(stock_symbol))
            try:
                data = self.time_series.get_intraday(symbol=stock_symbol,
                                                     outputsize="full",
                                                     interval="1min")[0]

            except ValueError as error:
                print(error)

                # TODO: handle cases where there is no symbol vs when AV tells us to slow down
                continue

            for index, row in data.iterrows():
                data_list = pandas_to_list(index, row)
                self.changes.append([stock_symbol] + data_list)


            # Hardcoded wait time to avoid AV throttling.
            # Apparently now you can't make calls as frequently as before :( Standard API
            # rate is 5 calls per minute.
            time.sleep(13)

        print("Fetched {} new datapoints".format(len(self.changes)))



    def commit(self):
        """Commits the changes in self.changes to the database."""

        # Currently we don't actually have any code for only writing the new stuff.
        # This function is more or less a prototype.

        if self.connection is None:
            raise Exception("No database connected to DataLoader. Use connect(db_path).")

        # TODO: resolve unique primary key collisions.
        self.connection.executemany("INSERT INTO prices VALUES (?,?,?,?,?,?,?,?)", self.changes)
        self.connection.commit()
