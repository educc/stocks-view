#!/bin/bash

source env/bin/activate

stocks_csv="./stocks/nasdaq_nyse.csv"
stock_data_dir="./data"
out_dir="./stock-order/nasdaq_nyse"

python src/sort_stocks_by_criteria/sort.py $stocks_csv $stock_data_dir $out_dir