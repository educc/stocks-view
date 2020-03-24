#!/bin/bash

source env/bin/activate

stocks="./stocks/nasdaq_nyse.csv"
data="./data"

python src/web_view_stocks/app.py $stocks $data