from Investment import Investment
import random as rand

class Portfolio:

    def __init__(self, portfolio) :
        self.portfolio = portfolio
        self.worth = sum(item.value for item in portfolio)

    def __str__(self):
        message = ""
        message += "\tSYMBOL     30-DAY CHANGE      START AMOUNT ($)     END AMOUNT ($)     PROFIT ($)\n"
        message += "\t------     -------------      ----------------     --------------     ----------\n"
        for investment in self.portfolio:
            message += "\t{:>6}     {:>12}%     {:>16}     {:>14}     {:>10}\n".format(
                investment.symbol, 
                round(investment.percent_change * 100, 2),
                round(investment.start_amount, 2),
                round(investment.value, 2),
                round(investment.value - investment.start_amount, 2)
                )
        return message

    def __lt__(self, other):
        return self.worth < other.worth

    def __le__(self, other):
        return self.worth <= other.worth

    def __gt__(self, other):
        return self.worth > other.worth
    
    def __ge__(self, other):
        return self.worth >= other.worth
    
    def __eq__(self, other):
        return self.worth == other.worth

    def get_neighbor(self, i, j):
        temp_portfolio = self.portfolio.copy()
        temp_portfolio[i] = Investment(self.portfolio[i].symbol, 
                                       self.portfolio[i].start_amount - (self.portfolio[i].start_amount * .1),
                                       self.portfolio[i].percent_change)
        temp_portfolio[j] = Investment(self.portfolio[j].symbol,
                                       self.portfolio[j].start_amount + (self.portfolio[i].start_amount * .1),
                                       self.portfolio[j].percent_change)
        return Portfolio(temp_portfolio)
    
    def get_best(self):
        best = self
        for i, invest in enumerate(self.portfolio):
            for j, other_invest in enumerate(self.portfolio):
                if i == j:
                    continue
                neighbor = self.get_neighbor(i, j)
                if neighbor > best:
                    best = neighbor
        return best

    def get_random_neighbor(self):
        neighbors = []
        for i, invest in enumerate(self.portfolio):
            for j, other_invest in enumerate(self.portfolio):
                if i == j:
                    continue
                neighbors.append(self.get_neighbor(i, j))
        return neighbors[rand.randint(0, len(neighbors) - 1)]
                