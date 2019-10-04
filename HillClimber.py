from Investment import Investment
from Portfolio import Portfolio
import random as rand

class HillClimber:
    def __init__(self, start_portfolio, num_restarts=10, total_investment=10000):
        self.start_portfolio = start_portfolio
        self.num_restarts = num_restarts
        self.total_investment = total_investment
    
    def random_restart(self):
        remaining = self.total_investment
        temp_portfolio = []
        for i, invest in enumerate(self.start_portfolio.portfolio):
            if i == 9:
                temp_portfolio.append(Investment(invest.symbol, remaining, invest.percent_change))
                break
            invest_amt = rand.randint(0, remaining)
            temp_portfolio.append(Investment(invest.symbol, invest_amt, invest.percent_change))
            remaining -= invest_amt
        return Portfolio(temp_portfolio)

    def hill_climb(self):
        best = self.start_portfolio
        current = self.start_portfolio
        while self.num_restarts > 0:
            while True:
                best = current.get_best()
                print(best)
                print(best.worth)
                if best <= current:
                    break
                current = best
            current = self.random_restart()
            self.num_restarts -= 1
        return best

    
