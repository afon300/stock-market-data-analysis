import yfinance as yf
import pandas as pd
import streamlit as st
from sqlalchemy import create_engine
import os

# Database configuration
DB_PATH = "sqlite:///market_data.db"
engine = create_engine(DB_PATH)

@st.cache_data(ttl=3600)
def fetch_stock_data(ticker, start_date, end_date):
    """
    Downloads historical market data from Yahoo Finance.
    Standardizes column names and handles multi-index headers.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date, progress=False)
        
        if not data.empty:
            # Standardize columns: yfinance often returns multi-index columns in newer versions
            if isinstance(data.columns, pd.MultiIndex):
                data.columns = data.columns.get_level_values(0)
            return data
        return None
    except Exception as e:
        st.error(f"Network Error: Unable to reach data provider for {ticker}.")
        return None

def save_to_db(data, ticker):
    """
    Persists historical data to a local SQLite database for offline analysis.
    """
    try:
        data.to_sql(ticker, engine, if_exists='replace')
    except Exception:
        pass # Silently fail if DB is locked or other issues

@st.cache_data(ttl=86400)  # Info doesn't change as often, cache for 24h
def fetch_ticker_info(ticker):
    """
    Fetches company information and fundamental data.
    """
    try:
        t = yf.Ticker(ticker)
        return t.info
    except Exception as e:
        return None

@st.cache_data(ttl=3600)
def fetch_ticker_news(ticker):
    """
    Fetches latest news for the given ticker.
    """
    try:
        t = yf.Ticker(ticker)
        return t.news
    except Exception:
        return []

def fetch_benchmark_data(benchmark_ticker="^GSPC", start_date=None, end_date=None):
    """
    Fetches benchmark data (e.g., S&P 500) for comparison.
    """
    data = yf.download(benchmark_ticker, start=start_date, end=end_date)
    
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)
    
    if 'Adj Close' in data.columns:
        return data['Adj Close']
    return data['Close']
