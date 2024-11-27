import yfinance as yf
import pandas as pd
import numpy as np

def calculate_sortino_ratio(ticker, start_date, end_date, risk_free_rate=0.02):
    """
    Calculate Sortino ratio for a given stock
    Parameters:
    ticker (str): Stock ticker symbol
    start_date (str): Start date in 'YYYY-MM-DD' format
    end_date (str): End date in 'YYYY-MM-DD' format
    risk_free_rate (float): Annual risk-free rate, default 2%
    """
    # Download stock data
    stock = yf.download(ticker, start=start_date, end=end_date)
    
    # Calculate daily returns
    daily_returns = stock['Adj Close'].pct_change()
    
    # Calculate average return (annualized)
    avg_return = daily_returns.mean() * 252
     
    #Store all returns that have negative values
    negative_daily_returns = daily_returns[daily_returns<0]

    # Calculate downside deviation of returns (annualized) 
    annualized_downside_dev = negative_daily_returns.std() * np.sqrt(252)
    
    # Calculate Sortino ratio
    sortino_ratio = (avg_return - risk_free_rate) / annualized_downside_dev
    
    return sortino_ratio