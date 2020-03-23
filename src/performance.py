import asyncio
import numpy as np
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
import time
import dateutil
import pandas

_MAX_WORKERS = 16
_MAX_REVENUE = 500
_MIN_REVENUE = 75
_DATA_PATH = "./data"
_OUT_STOCK_REVENUE = "stocks_revenue_ordered_desc.csv"
_FILENAME_STOCK_DESC = "stocks_desc.csv"

_COL_REVENUE = "revenue"
_COL_DATEATMONTH = "dateAtMonth"
_COL_STD = "std"



def read_stocks_desc():
    list_dict = pandas.read_csv(_FILENAME_STOCK_DESC, sep=";").to_dict("records")
    return { item["Symbol"]:item["Name"] for item in list_dict}

_STOCKS_DICT = read_stocks_desc()

def create_and_process_dataframe_from_csv(filename):
    df = pandas.read_csv(filename)

    col_group = _COL_DATEATMONTH

    df['Date'] = df['Date'].apply(dateutil.parser.parse)
    df['DateYear'] = df.apply(lambda x: x['Date'].strftime("%Y") , axis=1)
    df[col_group] = df.apply(lambda x: x['Date'].strftime("%Y%m") , axis=1)
    df = df.loc[df['DateYear'].isin( ("2018","2017","2016","2015") )]
    df = df.set_index(['Date'])

    df = df['Close'].groupby(df[col_group]).agg({
        "first": lambda x: x.iloc[0],
        "last":  lambda x: x.iloc[-1],
    })
    df[_COL_REVENUE] = df.apply( lambda x: x["last"]/x["first"]*100-100 , axis=1)
    return df

def create_dataframe(stock_name, filename_data_stock):
    try:
        df = create_and_process_dataframe_from_csv(filename_data_stock)
        
        #print(stock_name)
        
        total_revenue = df[_COL_REVENUE].sum()
        total_revenue = int(np.round(total_revenue)/10)*10

        if total_revenue < _MIN_REVENUE or total_revenue > _MAX_REVENUE:
            return None


        standard_deviation = df[_COL_REVENUE].std()
        standard_deviation = np.round(standard_deviation)

        if total_revenue != 0:
            return {
                "stock": stock_name,
                "stock_desc": _STOCKS_DICT[stock_name],
                _COL_REVENUE: total_revenue,
                _COL_STD: standard_deviation
            }
    except Exception as ex:
        print("Error at: " + stock_name, ex)
    return None

def add_result_to_queue(future, queue):
    aux = future.result()
    if not aux is None:
        queue.put(aux)


def main():
    start = time.time()

    myqueue = Queue()

    results = []
    with ProcessPoolExecutor(max_workers=_MAX_WORKERS) as executor:

        for filename in os.listdir(_DATA_PATH):
            absfilename = os.path.join(_DATA_PATH, filename)
            future = executor.submit(create_dataframe, filename, absfilename)
            future.add_done_callback(lambda fut: add_result_to_queue(fut, myqueue))
        executor.shutdown()
    #end-with

    data = []
    while not myqueue.empty():
        data.append(myqueue.get())
    
    df = pandas.DataFrame.from_dict(data)
    #df = df.sort_values([_COL_REVENUE, _COL_STD], ascending=[False, True])
    #df = df.sort_values(_COL_STD, ascending=True)
    df = df.sort_values([_COL_STD, _COL_REVENUE], ascending=[True, False])
    df.to_csv(_OUT_STOCK_REVENUE, columns=["stock","stock_desc",_COL_REVENUE, _COL_STD], index=False, sep=";")
    
    end_time = time.time()  
    print("Total time: {}".format(end_time - start))


if __name__ == "__main__":
    main()