class Portfolio:

    def __init__(self, portfolio) :
        self.portfolio = portfolio
        self.worth = sum(item.value for item in portfolio)