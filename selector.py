import os
import pandas
import dateutil

_DATA_PATH = "./data"
_OUT_STOCK_REVENUE = "stocks_revenue_ordered_desc_XX.csv"

def get_stats(group):
    return {'first': group.nth(0), 'last': group.max() }

def main():
    newdata = []
    for filename in os.listdir(_DATA_PATH):
        stockfilename = os.path.join(_DATA_PATH, filename)

        try:
            df = pandas.read_csv(stockfilename)
            df['Date'] = df['Date'].apply(dateutil.parser.parse)
            df['DateYear'] = df.apply(lambda x: x['Date'].strftime("%Y") , axis=1)
            df = df.loc[df['DateYear'].isin( ("2018","2017","2016","2015") )]
            df = df.set_index(['Date'])

            df = df['Close'].groupby(df['DateYear']).agg({
                "first": lambda x: x.iloc[0],
                "last":  lambda x: x.iloc[-1],
            })

            df['revenue'] = df.apply( lambda x: x["last"]/x["first"]*100-100 , axis=1)
            
            print("%s,%s" % (filename, df['revenue'].sum()))
            newdata.append({
                "stock": filename,
                "revenue": df['revenue'].sum()
            })
        except Exception as ex:
            print(filename, ex)
            continue
    #end-for

    df = pandas.DataFrame.from_dict(newdata)
    df = df.sort_values(by='revenue', ascending=False)
    df.to_csv(_OUT_STOCK_REVENUE)

if __name__ == "__main__":
    main()