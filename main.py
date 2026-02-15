import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
# Define the stock tickers to analyze
TICKERS = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
START_DATE = '2023-01-01'
END_DATE = '2024-01-01'

# Set visual style for Seaborn
sns.set_theme(style="darkgrid")

def fetch_financial_data(tickers, start_date, end_date):
    """
    Fetches historical stock data from Yahoo Finance API.
    """
    print(f"Fetching data for: {', '.join(tickers)}...")
    # 'Adj Close' is generally better for analysis as it accounts for dividends/splits
    data = yf.download(tickers, start=start_date, end=end_date)
    
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    return data['Close']

def clean_and_process_data(df):
    """
    Performs data cleaning and calculates financial metrics.
    1. Handles missing values.
    2. Calculates Daily Returns (percentage change).
    3. Calculates Rolling Volatility (standard deviation).
    """
    # 1. Data Cleaning: Drop any rows with missing values
    df_clean = df.dropna()
    
    # 2. Calculate Daily Returns
    daily_returns = df_clean.pct_change().dropna()
    
    return df_clean, daily_returns

def visualize_volatility(daily_returns):
    """
    Visualizes the distribution of daily returns (Volatility) using Seaborn.
    """
    plt.figure(figsize=(12, 6))
    
    # Using Histplot to show distribution (fat tails indicate volatility)
    for ticker in daily_returns.columns:
        sns.kdeplot(daily_returns[ticker], label=ticker, fill=True, alpha=0.3)
        
    plt.title('Distribution of Daily Returns (Volatility Analysis)')
    plt.xlabel('Daily Return')
    plt.ylabel('Density')
    plt.legend()
    plt.show()

def visualize_correlations(daily_returns):
    """
    Calculates and visualizes the correlation matrix between stocks.
    This serves as the 'Statistical Model' to identify relationships.
    """
    # Calculate correlation matrix
    corr_matrix = daily_returns.corr()
    
    plt.figure(figsize=(10, 8))
    
    # Heatmap visualization
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    
    plt.title('Stock Correlation Matrix')
    plt.show()

def visualize_trends(prices):
    """
    Simple line chart to see the price trends over time.
    """
    plt.figure(figsize=(14, 7))
    sns.lineplot(data=prices)
    plt.title('Stock Price Trends (Adjusted Close)')
    plt.ylabel('Price ($)')
    plt.xlabel('Date')
    plt.show()

# ---------------------------------------------------------
# Main Execution Flow
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        # Step 1: Data Retrieval
        stock_prices = fetch_financial_data(TICKERS, START_DATE, END_DATE)
        
        # Step 2: Cleaning & Processing
        clean_prices, stock_returns = clean_and_process_data(stock_prices)
        
        # Step 3: Visualization & Analysis
        print("Generating Price Trends chart...")
        visualize_trends(clean_prices)
        
        print("Generating Volatility analysis...")
        visualize_volatility(stock_returns)
        
        print("Generating Correlation Matrix...")
        visualize_correlations(stock_returns)
        
        print("Analysis complete.")
        
    except Exception as e:
        print(f"An error occurred: {e}")