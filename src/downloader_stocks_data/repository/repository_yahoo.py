import math
from datetime import datetime
from .repository import StockRepository
from .stock import StockIterable
from .stock import Stock
from pandas import DataFrame
import yfinance as yf

class YahooRepository(StockRepository):

    def __init__(self):
        self.name = "yahoo"

    def get(self, stock_name: str, date_start: datetime, date_end: datetime) -> StockIterable:
        data = yf.download(stock_name, start=date_start, end=date_end)
        return StockDateFrameIterable(stock_name, data)

class StockDateFrameIterable(StockIterable):

    def __init__(self, stock_name, df: DataFrame):
        self.it = df.itertuples()
        self.stock_name = stock_name

    def __iter__(self):
        return self
    
    def __next__(self):
        item = next(self.it)
        stock = Stock() 

        stock.name = self.stock_name
        stock.date = getattr(item, "Index").strftime("%Y-%m-%d")
        stock.open = getattr(item, "Open")
        stock.high = getattr(item, "High")
        stock.low = getattr(item, "Low")
        stock.close = getattr(item, "Close")
        stock.volume = getattr(item, "Volume")

        round_stock_numbers(stock, 2)

        return stock

def round_stock_numbers(stock: Stock, decimals):
    factor = math.pow(10, decimals)

    if stock.open:
        stock.open = round(stock.open * factor) / factor
    
    if stock.high:
        stock.high = round(stock.high * factor) / factor
    
    if stock.low:
        stock.low = round(stock.low * factor) / factor
    
    if stock.close:
        stock.close = round(stock.close * factor) / factor
    