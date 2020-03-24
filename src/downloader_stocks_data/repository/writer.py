from .stock import Stock
from .stock import StockIterable

SEPARATOR = ","
CACHE_SIZE_FOR_WRITE = 100
HEADERS = [p for p in vars(Stock()) if p != "name" ]

def header_line():
    return SEPARATOR.join(HEADERS) + "\n"

def repository_write_file(data: StockIterable, filename):
    cache = [header_line()]

    with open(filename, "w") as myfile:

        for stock in data:
            cache.append(_stock_to_line(stock))
            if len(cache) > CACHE_SIZE_FOR_WRITE:
                myfile.writelines(cache)
                cache = []
        #end

        if len(cache) > 0:
            myfile.writelines(cache)
    #end-with

def _stock_to_line(stock: Stock):
    value_list = [str(getattr(stock, it)) for it in HEADERS]
    return SEPARATOR.join(value_list) + "\n"