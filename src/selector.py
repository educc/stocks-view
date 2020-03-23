import os
import pandas
import dateutil
import time
from threading import current_thread
from rx import Observable
from rx.concurrency import ThreadPoolScheduler

_THREADS_POOL = 16
_REVENUE = "revenue"
_DATA_PATH = "./data"
_OUT_STOCK_REVENUE = "stocks_revenue_ordered_desc.csv"
_FILENAME_STOCK_DESC = "stocks_desc.csv"


pool_scheduler = ThreadPoolScheduler(_THREADS_POOL)


time_start = time.time()

def get_stats(group):
    return {'first': group.nth(0), 'last': group.max() }

def read_stocks_desc():
    list_dict = pandas.read_csv(_FILENAME_STOCK_DESC, sep=";").to_dict("records")
    return { item["Symbol"]:item["Name"] for item in list_dict}

def create_dataframe(tuplaStocks, stocks_dict, observer):
    try:
        stock_name = tuplaStocks[0]
        df = pandas.read_csv(tuplaStocks[1])
        df['Date'] = df['Date'].apply(dateutil.parser.parse)
        df['DateYear'] = df.apply(lambda x: x['Date'].strftime("%Y") , axis=1)
        df = df.loc[df['DateYear'].isin( ("2018","2017","2016","2015") )]
        df = df.set_index(['Date'])

        df = df['Close'].groupby(df['DateYear']).agg({
            "first": lambda x: x.iloc[0],
            "last":  lambda x: x.iloc[-1],
        })
        df[_REVENUE] = df.apply( lambda x: x["last"]/x["first"]*100-100 , axis=1)

        print(stock_name)
        
        total_revenue = df[_REVENUE].sum()

        if total_revenue != 0:
            observer.on_next({
                "stock": stock_name,
                "stock_desc": stocks_dict[stock_name],
                _REVENUE: total_revenue
            })
    except Exception as ex:
        print("Error at: " + stock_name, ex)
    finally:
        observer.on_completed()

def create_dataframe_obs(tupleStocks, stocks_dict):
    return Observable \
            .create(lambda observer: create_dataframe(tupleStocks, stocks_dict, observer))# \
            #.subscribe_on(pool_scheduler)

def create_csv(result):
    print("on create_csv")

    df = pandas.DataFrame.from_dict(result)
    df = df.sort_values(by=_REVENUE, ascending=False)
    df.to_csv(_OUT_STOCK_REVENUE, columns=["stock","stock_desc",_REVENUE], index=False, sep=";")
    
    time_end = time.time()
    print("Total time(s) = ", time_end - time_start)

def main():
    stocks_dict = read_stocks_desc()

    source = Observable.from_(os.listdir(_DATA_PATH)) \
                .map(lambda it: (it, os.path.join(_DATA_PATH, it))) \
                .flat_map(lambda it: create_dataframe_obs(it, stocks_dict)) \
                .to_list()
    
    source.subscribe(on_next=lambda value: create_csv(value))


if __name__ == "__main__":
    main()