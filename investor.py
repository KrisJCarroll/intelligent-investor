import json
import urllib.request as requests
import ssl
from time import time
from datetime import date, timedelta
from Portfolio import Portfolio
from Investment import Investment
from HillClimber import HillClimber

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
    while len(portfolio) < 10:
        yesterday = date.today() - timedelta(days=1)
        date_string = yesterday.strftime("%Y-%m-%d")

        thirty_days_ago = yesterday - timedelta(days=30)
        thirty_string = thirty_days_ago.strftime("%Y-%m-%d")
        potential_symbol = input("Input a valid NASDAQ stock symbol: ")
        if potential_symbol in portfolio:
            print("You already selected that symbol, let's diversify the portfolio! (Please enter unique symbols only)")
            continue

        query = "https://www.alphavantage.co/query?function={}&symbol={}&apikey={}".format(
                                            API_FUNCTION, potential_symbol, ALPHAVANTAGE_API_KEY)
        ssl_cert = ssl.SSLContext()
        thirty_day_history = requests.urlopen(query, context=ssl_cert)
        json_data = json.loads(thirty_day_history.read())

        if 'Error Message' in json_data:
            print("\tInvalid stock symbol, only valid NASDAQ stock symbols allowed!")
            continue
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
    start_portfolio = Portfolio(portfolio)
    print("\nHere is the portfolio I will optimize an investment mix in:")
    print(start_portfolio)

    start = time()
    print("Calculating optimal investment mix with hill-climbing (random restarts)...")
    climber = HillClimber(start_portfolio, 30, invest_amount)
    hill_best = climber.hill_climb()
    end = time()
    print("Done in {} seconds.\n".format(end-start))
    print(hill_best)
    print(hill_best.worth)

    start = time()
    print("Calculating optimal investment mix with simulated annealing...")
    # simulated annealing
    end = time()
    print("Done in {} seconds.\n".format(end-start))

    print("\n\n\n")
    print("Strategy         $ Profit")
    print("With your current investment strategy, you made: ${}".format(round(start_portfolio.worth - invest_amount, 2)))
        


