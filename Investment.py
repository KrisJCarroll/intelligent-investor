"""
Investment.py
Authors: Kristopher Carroll & Andrea Jacuk
CSCE A405 - Assignment 2

Basic class for storing Investment information such as stock symbol, starting investment amount,
and the 30-day change. Calculates the value of the investment after the 30-day change is applied.
"""

class Investment:

    def __init__(self, symbol, start_amount, percent_change):
        self.symbol = symbol
        self.start_amount = start_amount
        self.percent_change = percent_change
        self.value = round((self.start_amount * self.percent_change) + self.start_amount, 2)
    