
class Stock(object):
    
    def __init__(self):
        self.name = None
        self.date = None
        self.open = None
        self.high = None
        self.low = None
        self.close = None
        self.volume = None

class StockIterable:

    def __iter__(self):
        return self
    
    def __next__(self):
        raise StopIteration