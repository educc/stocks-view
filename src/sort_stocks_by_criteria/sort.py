import sys
import os
import csv
from typing import List
from operator import attrgetter
from stock import Stock
from itertools import groupby
from stock import StockOrder
from process_criteria import ProcessCriteriaBatchBuilder
from process_criteria_executor import execution_in_parallel

DELIMITER = "\t"

def stock_list(filename) -> List[Stock]:
    result = []
    with open(filename) as csvfile:
        reader = csv.reader(csvfile, delimiter=DELIMITER)
        for row in reader:
            result.append(Stock(row[0], row[1]))
    return result

def write_csv_from_stock_order_list(filename, stocks_order):
    
    with open(filename, "w") as myfile:
        writer = csv.writer(myfile)
        writer.writerows([it.to_list() for it in stocks_order])

def write_stock_order_list(stocks_order: List[StockOrder], out_dir: str):
    sorted_input = sorted(stocks_order, key=attrgetter("criteria_name"))
    groups = groupby(sorted_input, key=attrgetter("criteria_name"))
    
    for key, group in groups:
        filename = os.path.join(out_dir, key) + ".csv"
        ordered_list = sorted(list(group), key=attrgetter("order"), reverse=True)
        write_csv_from_stock_order_list(filename, ordered_list)

def main(stock_csv, stock_data_dir, stock_out_dir):
    stocks = stock_list(stock_csv)
    builder = ProcessCriteriaBatchBuilder(stocks, stock_data_dir)
    data = execution_in_parallel(builder.iter_process_criteria())

    write_stock_order_list(data, stock_out_dir)

if __name__ == "__main__":
    if len(sys.argv) <= 3:
        print("It required more params")
        print("python downloader.py STOCK_LIST_CSV STOCK_DATA_FOLDER STOCK_ORDER_OUTPUT_FOLDER")
        print("example")
        print("python sort.py nyse.csv ./data ./stock-order/nyse")
    else:
        stock_csv = sys.argv[1]
        stock_data_dir = sys.argv[2]
        stock_out_dir = sys.argv[3]

        if not os.path.exists(stock_csv):
            raise Exception("doesn't exists: " + stock_csv)

        if not os.path.exists(stock_data_dir):
            raise Exception("doesn't exists: " + stock_data_dir)

        if not os.path.exists(stock_out_dir):
            raise Exception("doesn't exists: " + stock_out_dir)
        
        main(stock_csv, stock_data_dir, stock_out_dir)