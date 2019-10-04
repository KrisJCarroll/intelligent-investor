from Investment import Investment
from Portfolio import Portfolio
import random as rand

class HillClimber:
    def __init__(self, start_portfolio, num_restarts=10, total_investment=10000):
        self.start_portfolio = start_portfolio
        self.num_restarts = num_restarts
        self.total_investment = total_investment
    
    def random_restart(self):

        return

    def hill_climb(self):
        best = self.start_portfolio
        current = self.start_portfolio
        temp_portfolio = current.portfolio.copy()
        while self.num_restarts > 0:
            while True:
                best = current.get_best()
                print(best)
                print(best.worth)
                if best <= current:
                    break
                current = best
            self.random_restart()
            self.num_restarts -= 1
        return best

    
