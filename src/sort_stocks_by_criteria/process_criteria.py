import os
import pandas as pd
from stock import Stock
from stock import StockOrder
from typing import List
from criteria import Criteria
from criteria import all_criteria


class ProcessCriteria:

    def __init__(self, stock_data_filename: str, desc, criteria: Criteria):
        self.stock_data_filename = stock_data_filename
        self.description = desc
        self.criteria = criteria

    def process(self) -> StockOrder:
        try:
            df = pd.read_csv(self.stock_data_filename)
        except Exception as e:
            msg = self.stock_data_filename + ": " + str(e)
            print("WARNING: " + msg)
            return None
        if len(df) == 0: return None

        order = self.criteria.process(df)

        if order is None: return None

        return StockOrder(self.symbol(), self.description, order, self.criteria.name())

    def symbol(self):
        filename = os.path.splitext(self.stock_data_filename)[0]
        filename = os.path.basename(filename)
        return filename

class ProcessCriteriaBatchBuilder:

    def __init__(self, stock_list: List[Stock], stock_directory):
        self.stock_directory = stock_directory
        self.stock_list = stock_list

    def iter_process_criteria(self):
        for item in self.stock_list:
            symbol = item.symbol
            desc = item.description
            absfile = os.path.join(self.stock_directory, symbol)

            for criteria in all_criteria():
                yield ProcessCriteria(absfile, desc, criteria)