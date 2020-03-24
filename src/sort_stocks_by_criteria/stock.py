
class Stock:

    def __init__(self, symbol, desc):
        self.symbol = symbol
        self.description = desc


class StockOrder:

    def __init__(self, symbol, desc, order, criteria_name):
        self.symbol = symbol
        self.criteria_name = criteria_name
        self.order = order
        self.description = desc

    def to_list(self):
        return [
            self.symbol,
            self.description,
            self.order
        ]

    def __str__(self):
        return "{0}\t{2} {3} - {1}".format( \
            self.symbol, self.description, self.criteria_name, self.order)