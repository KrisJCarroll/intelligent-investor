import random as rand
import math
from Investment import Investment
from Portfolio import Portfolio

class Annealer:
    def __init__(self, start_portfolio, max_temp=100000):
        self.start_portfolio = start_portfolio
        self.max_temp = max_temp
    
    def anneal(self):
        temp = self.max_temp
        current = self.start_portfolio
        while temp > 0:
            next = current.get_random_neighbor()
            error = next.worth - current.worth
            if error > 0:
                current = next
            else:
                if math.exp(error/temp) < rand.random():
                    current = next
            temp -= 1
        return current
