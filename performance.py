import asyncio
from queue import Queue
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os
import time
import dateutil
import pandas

_DATA_PATH = "./data"
_OUT_STOCK_REVENUE = "stocks_revenue_ordered_desc.csv"
_FILENAME_STOCK_DESC = "stocks_desc.csv"
_REVENUE = "revenue"


def read_stocks_desc():
    list_dict = pandas.read_csv(_FILENAME_STOCK_DESC, sep=";").to_dict("records")
    return { item["Symbol"]:item["Name"] for item in list_dict}

_STOCKS_DICT = read_stocks_desc()

def create_and_process_dataframe_from_csv(filename):
    df = pandas.read_csv(filename)

    df['Date'] = df['Date'].apply(dateutil.parser.parse)
    df['DateYear'] = df.apply(lambda x: x['Date'].strftime("%Y") , axis=1)
    df = df.loc[df['DateYear'].isin( ("2018","2017","2016","2015") )]
    df = df.set_index(['Date'])

    df = df['Close'].groupby(df['DateYear']).agg({
        "first": lambda x: x.iloc[0],
        "last":  lambda x: x.iloc[-1],
    })
    df[_REVENUE] = df.apply( lambda x: x["last"]/x["first"]*100-100 , axis=1)
    return df

def create_dataframe(stock_name, filename_data_stock):
    try:
        df = create_and_process_dataframe_from_csv(filename_data_stock)
        
        print(stock_name)
        
        total_revenue = df[_REVENUE].sum()

        if total_revenue != 0:
            return {
                "stock": stock_name,
                "stock_desc": _STOCKS_DICT[stock_name],
                _REVENUE: total_revenue
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
    with ProcessPoolExecutor(max_workers=8) as executor:

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
    df = df.sort_values(by=_REVENUE, ascending=False)
    df.to_csv(_OUT_STOCK_REVENUE, columns=["stock","stock_desc",_REVENUE], index=False, sep=";")
    
    end_time = time.time()  
    print("Total time: {}".format(end_time - start))


if __name__ == "__main__":
    main()