import yfinance as yf
import pandas as pd
import numpy as np

def calculate_sharpe_ratio(ticker, start_date, end_date, risk_free_rate=0.02):
    """
    Calculate Sharpe ratio for a given stock
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
    
    # Calculate standard deviation of returns (annualized)
    annualized_std_dev = daily_returns.std() * np.sqrt(252)
    
    # Calculate Sharpe ratio
    sharpe_ratio = (avg_return - risk_free_rate) / annualized_std_dev
    
    return sharpe_ratio

# Example usage
if __name__ == "__main__":
    # Get S&P 500 tickers
    sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    tickers = sp500['Symbol'].tolist() #convert to standard python list
    
    # Calculate Sharpe ratio for each stock
    results = {}
    for ticker in tickers[:10]:  # Example with first 10 stocks
        try:
            sharpe = calculate_sharpe_ratio(ticker, 
                                           start_date='2000-01-01', 
                                           end_date='2023-12-31')
            results[ticker] = sharpe
        except:
            print(f"Error calculating Sharpe ratio for {ticker}")
    
    # Convert results to DataFrame and sort
    sharpe_df = pd.DataFrame.from_dict(results, orient='index', columns=['Sharpe Ratio'])
    sharpe_df = sharpe_df.sort_values('Sharpe Ratio', ascending=False)
    
    print("\nTop 5 stocks by Sharpe Ratio:")
    print(sharpe_df.head())