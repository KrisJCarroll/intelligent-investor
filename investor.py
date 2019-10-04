"""
investor.py
Authors: Kristopher Carroll & Andrea Jacuk
CSCE A405 - Assignment 2

This program intelligently invests amongst a portfolio of 10 different NASDAQ traded stocks.
Originally intended to be limited to the Dow Jones Industrial Average 30, the use of an API
servering JSON files allows for realtime data to be loaded for any valid NASDAQ company.

Users will be prompted to enter 10 different companies and a total investment amount for the
portfolio. Then, the investment portfolio is optimized according to 3 different approaches.
    Trust Fund Baby - investment evenly distributed across portfolio
    Hill-Climb(Random Restart) - searches for maxima and performs random restarts, looking for
        the best overall
    Simulated Annealing - allows for large random movement initially but slowly narrows the 
        chance that new moves will be selected, resulting in resting at local maxima

Results of each investment strategy are output at the end of the run, as well as printouts of 
the maximized portfolio found by each approach.
"""

import json
import urllib.request as requests
import ssl
from time import time
from datetime import date, timedelta
from Portfolio import Portfolio
from Investment import Investment
from HillClimber import HillClimber
from Annealer import Annealer

ALPHAVANTAGE_API_KEY = "LAWBJ72TZRI6BMNI"
API_FUNCTION = "TIME_SERIES_DAILY"
FUNC_STRING = "Time Series (Daily)"

class Main:
    portfolio = []

    print("======================================================================================================")
    print("Welcome to the Intelligent Investor(tm). You provide 10 stocks for a portfolio you'd like to optimize.")
    print("I'll tell you what the best mix of investment in those 10 stocks would be based on 30-day history.")
    print("Results will be calculated based on either hill-climbing or simulated annealing algorithms.")
    print("======================================================================================================")
    invest_amount = round(float(input("Enter dollar amount to invest: $")), 2)
    
    
    # We're going to query the AlphaVantage API to get realtime 30-day changes
    # Only valid NASDAQ stock symbols will work for the API but errors are handled gracefully
    # and the user is reprompted to enter a new symbol until 10 stocks have been chosen successfully
    while len(portfolio) < 10:
        yesterday = date.today() - timedelta(days=1)
        date_string = yesterday.strftime("%Y-%m-%d")

        thirty_days_ago = yesterday - timedelta(days=30)
        thirty_string = thirty_days_ago.strftime("%Y-%m-%d")
        potential_symbol = input("Input a valid NASDAQ stock symbol: ")
        if potential_symbol in portfolio:
            print("You already selected that symbol, let's diversify the portfolio! (Please enter unique symbols only)")
            continue

        # building the query according to API format
        query = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(
                                            API_FUNCTION, potential_symbol, ALPHAVANTAGE_API_KEY)
        ssl_cert = ssl.SSLContext() # required to use https
        thirty_day_history = requests.urlopen(query, context=ssl_cert)
        json_data = json.loads(thirty_day_history.read()) # load the json as a dict

        # invalid stock symbol
        if 'Error Message' in json_data:
            print("\tInvalid stock symbol, only valid NASDAQ stock symbols allowed!")
            continue

        # search for 30-day change, not all days have an entry (weekends are absent) so
        # some adjustments must be done to perform well across all days used
        closed = False
        while not closed:
            try:
                last_close = json_data["Time Series (Daily)"][date_string]["4. close"]
                closed = True
            except KeyError:
                yesterday = yesterday - timedelta(days=1)
                date_string = yesterday.strftime("%Y-%m-%d")

                thirty_days_ago = yesterday - timedelta(days=30)
                thirty_string = thirty_days_ago.strftime("%Y-%m-%d")
        closed = False
        # make sure the 30 day change is appropriate length
        while not closed:
            try:
                thirty_close = json_data[FUNC_STRING][thirty_string]["4. close"]
                closed = True
            except KeyError:
                thirty_days_ago = thirty_days_ago - timedelta(days=1)
                thirty_string = thirty_days_ago.strftime("%Y-%m-%d")
            
        thirty_day_change =  (float(last_close) - float(thirty_close)) / float(thirty_close)
        portfolio.append(Investment(potential_symbol, invest_amount / 10, thirty_day_change))
        
        print("Successfully loaded data for {} and added to portfolio.\n".format(potential_symbol))

    # here we go...output the portfolio with Trust Fund Baby approach
    start_portfolio = Portfolio(portfolio)
    print("\nHere is the portfolio I will optimize an investment mix in:")
    print(start_portfolio)

    # now do Hill Climbing with random restarts and print the corresponding optimized Portfolio
    start = time()
    print("Calculating optimal investment mix with hill-climbing (random restarts)...")
    climber = HillClimber(start_portfolio, 10, invest_amount)
    hill_best = climber.hill_climb()
    end = time()
    print("Done in {} seconds.\n".format(end-start))
    print(hill_best)

    # finally do Simulated Annealing and print corresponding optimized Portfolio
    start = time()
    print("Calculating optimal investment mix with simulated annealing...")
    annealer = Annealer(start_portfolio, 1000000)
    anneal_best = annealer.anneal()
    print(anneal_best)
    end = time()
    print("Done in {} seconds.\n".format(end-start))

    print("\n\n")
    print("Strategy         $ Profit")
    print("--------         --------")
    print("  {:>3}             {:>7}".format("TFB", round(start_portfolio.worth - invest_amount, 2)))
    print("  {:>3}             {:>7}".format("HC", round(hill_best.worth - invest_amount, 2)))
    print("  {:>3}             {:>7}".format("SA", round(anneal_best.worth - invest_amount, 2)))

        


