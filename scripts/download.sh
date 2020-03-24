#!/bin/bash

source env/bin/activate

start="2019-03-23"
end="2020-03-23"
output="./data"

input="./stocks/nasdaq_nyse.csv"
IFS=$'\n'
for stock in $(cut -f1 ./stocks/nasdaq_nyse.csv)
do
    echo stock = $stock
    python src/downloader_stocks_data/downloader.py yahoo $stock $start $end $output
done