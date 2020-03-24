import os
import pandas

SEPARATOR_STOCKS_LIST = "\t"

class StockData:

    def __init__(self, stock_list_filename, data_dir):
        self.stock_list_filename = stock_list_filename
        self.data_dir = data_dir

    def stock_list(self):
        df = pandas.read_csv(self.stock_list_filename, delimiter=SEPARATOR_STOCKS_LIST)
        r = [{'label': it.Description, 'value': it.Symbol } for it in df.itertuples()]
        return r

    def history(self, stock_symbol: str):
        filename = os.path.join(self.data_dir, stock_symbol)
        if not os.path.exists(filename):
            raise Exception("Data for stock doesn't exists")

        df = pandas.read_csv(filename, delimiter=",")
        return [{
                'x': df.date,
                'y': df.close
        }]
        