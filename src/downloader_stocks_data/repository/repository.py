from datetime import datetime
from .stock import StockIterable

class StockRepository:

    def __init__(self):
        self.name = ""

    def get(self, stock_name: str, date_start: datetime, date_end: datetime) -> StockIterable:
        pass
