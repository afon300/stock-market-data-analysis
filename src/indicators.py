import pandas as pd
import pandas_ta as ta
import numpy as np

def add_technical_indicators(df):
    """
    Computes a comprehensive suite of technical indicators using pandas-ta.
    
    Includes:
    - Trend: SMA (20, 50)
    - Momentum: RSI (14)
    - Volatility: Bollinger Bands, MACD
    - Returns: Percentage daily change
    """
    df = df.copy()
    
    # Ensure data is numeric
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    
    # Trend Indicators: Simple Moving Averages
    df['SMA_20'] = ta.sma(df['Close'], length=20)
    df['SMA_50'] = ta.sma(df['Close'], length=50)
    
    # MACD: Trend and Momentum oscillator
    macd = ta.macd(df['Close'])
    if macd is not None:
        df = pd.concat([df, macd], axis=1)
    
    # RSI: Relative Strength Index for overbought/oversold conditions
    df['RSI'] = ta.rsi(df['Close'], length=14)
    
    # ATR: Average True Range for volatility
    df['ATR'] = ta.atr(df['High'], df['Low'], df['Close'], length=14)
    
    # Volatility: Bollinger Bands
    bbands = ta.bbands(df['Close'], length=20, std=2)
    if bbands is not None:
        df = pd.concat([df, bbands], axis=1)
    
    # Daily Returns for performance and risk analysis
    df['Daily_Return'] = df['Close'].pct_change()
    
    return df

def calculate_portfolio_metrics(df, quantity, initial_price):
    """
    Calculates key performance indicators (KPIs) and risk metrics for a position.
    
    Utilizes Historical Simulation for Value at Risk (VaR).
    """
    current_price = df['Close'].iloc[-1]
    pnl = (current_price - initial_price) * quantity
    pnl_percent = ((current_price / initial_price) - 1) * 100
    
    # Value at Risk (VaR) - 95% Confidence Level
    # Simple historical simulation method
    var_95 = np.percentile(df['Daily_Return'].dropna(), 5) * (current_price * quantity)
    
    return {
        "Current Value": current_price * quantity,
        "P&L": pnl,
        "P&L %": pnl_percent,
        "VaR (95%)": var_95
    }
