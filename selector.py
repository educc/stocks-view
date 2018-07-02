import os
import pandas
import dateutil

_DATA_PATH = "./data"

def get_stats(group):
    return {'first': group.nth(0), 'last': group.max() }

def main():
    newdata = []
    for filename in os.listdir(_DATA_PATH):
        stockfilename = os.path.join(_DATA_PATH, filename)

        df = pandas.read_csv(stockfilename)
        df['Date'] = df['Date'].apply(dateutil.parser.parse)
        df['DateYear'] = df.apply(lambda x: x['Date'].strftime("%Y") , axis=1)
        df = df.set_index(['Date'])

        df = df['Close'].groupby(df['DateYear']).agg({
            "first": lambda x: x.iloc[0],
            "last":  lambda x: x.iloc[-1],
        })

        df['revenue'] = df.apply( lambda x: x["last"]/x["first"]*100-100 , axis=1)
        
        #print(filename, df)
        print("%s,%s" % (filename, df['revenue'].sum()))
        newdata.append({
            "stock": filename,
            "revenue": df['revenue'].sum()
        })
    #end-for

    #df = pandas.DateFrame(newdata)
    #print(df)

if __name__ == "__main__":
    main()