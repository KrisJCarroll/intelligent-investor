"""
Annealer.py
Authors: Kristopher Carroll & Andrea Jacuk
CSCE A405 - Assignment 2

Class for managing simulated annealing search for optimal maxima. Annealer maintains
the starting Portfolio as well as the maximum temperature that should be used while
annealing.
"""

import random as rand
import math
from Investment import Investment
from Portfolio import Portfolio

class Annealer:
    def __init__(self, start_portfolio, max_temp=1000000):
        self.start_portfolio = start_portfolio
        self.max_temp = max_temp
    
    def anneal(self):
        temp = self.max_temp
        current = self.start_portfolio
        k = 0
        while temp > 0:
            next = current.get_random_neighbor()
            error = next.worth - current.worth
            if error > 0:
                current = next
            else:
                if math.exp(-error/temp) < rand.random():
                    current = next
            temp = int(self.max_temp * (0.99 ** k))
            k += 1
        return current
