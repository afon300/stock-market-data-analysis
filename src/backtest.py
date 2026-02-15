import pandas as pd
import numpy as np

def run_backtest(df, strategy_name="RSI Oversold"):
    """
    Simulates execution of trading strategies on historical data.
    
    Strategies:
    - RSI Oversold: Mean reversion (Buy < 30, Sell > 70)
    - SMA Crossover: Momentum (Buy SMA20 > SMA50)
    """
    data = df.copy()
    data['Signal'] = 0
    
    if strategy_name == "RSI Oversold":
        # Entry/Exit signals based on momentum extremes
        data.loc[data['RSI'] < 30, 'Signal'] = 1
        data.loc[data['RSI'] > 70, 'Signal'] = -1
    
    elif strategy_name == "SMA Crossover":
        # Trend-following signals based on moving average crossovers
        if 'SMA_20' in data.columns and 'SMA_50' in data.columns:
            data['Signal'] = np.where(data['SMA_20'] > data['SMA_50'], 1, -1)
    
    # Position tracking: forward fill signals to maintain position
    data['Position'] = data['Signal'].replace(0, np.nan).ffill().fillna(0)
    
    # Performance calculation: shift by 1 to avoid look-ahead bias
    data['Strategy_Return'] = data['Position'].shift(1) * data['Daily_Return']
    
    # Cumulative performance tracking
    data['Cum_Market_Return'] = (1 + data['Daily_Return'].fillna(0)).cumprod()
    data['Cum_Strategy_Return'] = (1 + data['Strategy_Return'].fillna(0)).cumprod()
    
    # Key Performance Indicators
    total_return = (data['Cum_Strategy_Return'].iloc[-1] - 1) * 100
    market_return = (data['Cum_Market_Return'].iloc[-1] - 1) * 100
    
    # Risk Metrics: Maximum Drawdown
    rolling_max = data['Cum_Strategy_Return'].cummax()
    drawdown = (data['Cum_Strategy_Return'] / rolling_max - 1).min() * 100
    
    # Accuracy: Percentage of profitable signals
    trades = data[data['Strategy_Return'] != 0]
    win_rate = (trades[trades['Strategy_Return'] > 0].shape[0] / trades.shape[0]) * 100 if not trades.empty else 0

    return {
        "Total Return (%)": total_return,
        "Market Return (%)": market_return,
        "Max Drawdown (%)": drawdown,
        "Win Rate (%)": win_rate,
        "Equity Curve": data[['Cum_Strategy_Return', 'Cum_Market_Return']]
    }
