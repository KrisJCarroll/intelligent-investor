class Investment:

    def __init__(self, symbol, start_amount, percent_change):
        self.symbol = symbol
        self.start_amount = start_amount
        self.percent_change = percent_change
        self.value = round((self.start_amount * self.percent_change) + self.start_amount, 2)
    