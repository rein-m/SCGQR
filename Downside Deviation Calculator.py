pip install yfinance pandas matplotlib
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def downside_deviation(ticker, start_date, end_date, mar):
    #need to declare mar(minimum acceptable return) - most commonly is zero or 1 or the risk free T-bill rate for the year (dependent on which year or years we are analyzing the data from))

    #imports data from yf
    stock_data = yf.Ticker(ticker).history(start=start_date, end=end_date)

    if stock_data.empty:
        print(f"No data available in {ticker}")
        return None

    if 'Adj Close' not in stock_data.columns:
        print(f"Coloumn 'Adj Close' missing in data for ticker symbol stock {ticker})
        return None

    # above code iterates to check if there is missing data within yf

    #start calculating daily returns - pct_change is from pandas %change formula
    stock_data['Return'] = stock_data['Adj Close'].pct_change()

    if stock_data['Return'].isnull().all():
        print(f"Error: Unable to calculate returns for ticker '{ticker}'.")
        return None
    #above checks if the return through pct.change is calculatable

    #using boolean to calculate downside deviation - formula given by sqrrt of the sums of all the negative ROI through subtracting the mar divided by the number of periods (how many of them are ROI < mar)
    stock_data['Downside'] = np.where(stock_data['Return'] < mar, (mar - stock_data['Return'])**2, 0)

    downside_deviation = np.sqrt(stock_data['Downside'].mean()*252)
    #252 b/c that is the no. of trading days per annum, annualizing the downside deviation calculations

    return downside_deviation

def plot_downside_deviation(stock_data, ticker, start_date, end_date):
    #want to plot out the downside deviation for a given stock by taking daily returns and the annualized downside deviation of such data

if __name__ == "__main__":
    #ticker test case given by chatgpt
    ticker = "AAPL"  # Apple Inc.
    start_date = "2020-01-01"
    end_date = "2023-12-31"
    mar = 0  # Minimum acceptable return - change if necessary

    downside_deviation = calculate_downside_deviation(ticker, start_date, end_date, mar)

    if downside_deviation is not None:
        print(f"Downside Deviation for {ticker} from {start_date} to {end_date}: {downside_deviation:.4f}")
    else:
        print(f"Failed to calculate downside deviation for {ticker}.")



# import yfinance as yahooFinance
#
# # Here We are getting Facebook financial information
# # We need to pass FB as argument for that
# GetFacebookInformation = yahooFinance.Ticker("META")
#
# # whole python dictionary is printed here
# print(GetFacebookInformation.info)