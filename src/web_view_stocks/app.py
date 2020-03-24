import sys
import os
from web import start_web
from data import StockData

def main(stock_list_filename, data_dir):
    stock_data = StockData(stock_list_filename, data_dir)
    
    start_web(stock_data)


if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print("more parameters are requiered")
        print("python app.py STOCK_FILE DATA_STOCKS")
        print("example")
        print("python app.py nyse.csv ./data")
    else:
        stock_filename = sys.argv[1]
        data_dir = sys.argv[2]

        if not os.path.exists(stock_filename):
            raise Exception("stock_filename doesn't exists: " + stock_filename)

        if not os.path.exists(data_dir):
            raise Exception("data_stocks doesn't exists: " + data_dir)

        main(stock_filename, data_dir)
