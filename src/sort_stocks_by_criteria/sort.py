import sys
import os
import csv
from typing import List
from stock import Stock
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

def main(stock_csv, stock_data_dir, stock_out_dir):
    stocks = stock_list(stock_csv)
    builder = ProcessCriteriaBatchBuilder(stocks, stock_data_dir)
    data = execution_in_parallel(builder.iter_process_criteria())

    for it in data:
        print(str(it))

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