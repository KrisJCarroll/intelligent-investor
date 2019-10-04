"""
Portfolio.py
Authors: Kristopher Carroll & Andrea Jacuk
CSCE A405 - Assignment 2

Class to hold Portfolios of 10 Investments selected by the user.
Stores the portfolio as a list of Investments as well as calculates the value of the portfolio
after the 30-day change is applied for comparison in search.
"""

from Investment import Investment
import random as rand

class Portfolio:

    def __init__(self, portfolio) :
        self.portfolio = portfolio
        self.worth = sum(item.value for item in portfolio)

    # Overloading the string representation of the Portfolio to allow print()'ing with desired format
    def __str__(self):
        message = ""
        message += "\tSYMBOL     30-DAY CHANGE      START AMOUNT ($)     END AMOUNT ($)     PROFIT ($)\n"
        message += "\t------     -------------      ----------------     --------------     ----------\n"
        for investment in self.portfolio:
            message += "\t{:>6}     {:>12}%      {:>16}      {:>14}      {:>10}\n".format(
                investment.symbol, 
                round(investment.percent_change * 100, 2),
                round(investment.start_amount, 2),
                round(investment.value, 2),
                round(investment.value - investment.start_amount, 2)
                )
        return message

    # Overloading the equality comparison operators to allow Portfolios to be compared
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

    # Takes two positions in the portfolio, i and j, and returns the neighbor Portfolio that results in
    # decreasing the starting investment amount of Investment i by 10% and increasing the investment
    # amount of Investment j by that amount.
    # Returns a new Portfolio created with the changes made.
    def get_neighbor(self, i, j):
        temp_portfolio = self.portfolio.copy()
        temp_portfolio[i] = Investment(self.portfolio[i].symbol, 
                                       self.portfolio[i].start_amount - (self.portfolio[i].start_amount * .1),
                                       self.portfolio[i].percent_change)
        temp_portfolio[j] = Investment(self.portfolio[j].symbol,
                                       self.portfolio[j].start_amount + (self.portfolio[i].start_amount * .1),
                                       self.portfolio[j].percent_change)
        return Portfolio(temp_portfolio)
    
    # Gets the best neighbor out of all possible neighbors a Portfolio can have (90 neighbors for 10 Investments
    # in Portfolio). The best neighbor is selected by comparing the Portfolio worth (the value of the Portfolio
    # after the 30 day change).
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

    # Returns a random neighbor Portfolio from all possible neighbors (90 total for 10 Investments in Portfolio).
    def get_random_neighbor(self):
        neighbors = []
        for i, invest in enumerate(self.portfolio):
            for j, other_invest in enumerate(self.portfolio):
                if i == j:
                    continue
                neighbors.append(self.get_neighbor(i, j))
        return neighbors[rand.randint(0, len(neighbors) - 1)]
                