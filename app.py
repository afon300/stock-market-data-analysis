import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

from src.data_loader import fetch_stock_data, fetch_benchmark_data, fetch_ticker_info, fetch_ticker_news, save_to_db
from src.indicators import add_technical_indicators, calculate_portfolio_metrics
from src.models import predict_next_days
from src.sentiment import analyze_sentiment
from src.backtest import run_backtest

st.set_page_config(page_title="FinAI Platform", page_icon="🏦", layout="wide")

# Sidebar Configuration
st.sidebar.title("🏦 FinAI Platform")

market_type = st.sidebar.selectbox("Market Type", ["Stocks", "Crypto", "Forex", "Commodities"])

# Set default tickers and placeholders based on market
if market_type == "Stocks":
    default_ticker = "AAPL"
    placeholder = "e.g. MSFT, TSLA"
elif market_type == "Crypto":
    default_ticker = "BTC-USD"
    placeholder = "e.g. ETH-USD, SOL-USD"
elif market_type == "Forex":
    default_ticker = "EURUSD=X"
    placeholder = "e.g. GBPUSD=X, JPY=X"
else: # Commodities
    default_ticker = "GC=F"
    placeholder = "e.g. CL=F (Oil), SI=F (Silver)"

ticker = st.sidebar.text_input("Asset Ticker", value=default_ticker, help=placeholder).upper()
days_history = st.sidebar.slider("Historical Data (Days)", 30, 730, 365)
start_date = datetime.now() - timedelta(days=days_history)
end_date = datetime.now().date()

# Load Data
print(f"--- Fetching data for {ticker} ---")
df = fetch_stock_data(ticker, start_date, end_date)

# Define currency symbol based on ticker/market
currency_symbol = "€" if "EUR" in ticker else "£" if "GBP" in ticker else "¥" if "JPY" in ticker else "$"

if df is not None:
    print(f"Successfully loaded {len(df)} rows.")
    save_to_db(df, ticker)
    df = add_technical_indicators(df)
    print("Technical indicators added.")
    
    # --- HEADER & METRICS ---
    st.markdown(f"## 📊 {ticker} Market Intelligence")
    
    # Quick Summary Metrics
    m1, m2, m3, m4 = st.columns(4)
    price = df['Close'].iloc[-1]
    change = price - df['Close'].iloc[-2]
    pct_change = (change / df['Close'].iloc[-2]) * 100
    
    m1.metric("Current Price", f"{currency_symbol}{price:.2f}", f"{change:+.2f} ({pct_change:+.2f}%)")
    m2.metric("Volume", f"{df['Volume'].iloc[-1]:,.0f}")
    m3.metric("RSI (14)", f"{df['RSI'].iloc[-1]:.2f}", "Overbought" if df['RSI'].iloc[-1] > 70 else "Oversold" if df['RSI'].iloc[-1] < 30 else "Neutral", delta_color="inverse" if df['RSI'].iloc[-1] > 70 or df['RSI'].iloc[-1] < 30 else "normal")
    m4.metric("Volatility (ATR)", f"{df.get('ATR', [0])[-1]:.2f}" if 'ATR' in df.columns else "N/A")

    st.divider()

    # Portfolio Section (Optional)
    with st.sidebar.expander("💼 My Portfolio"):
        qty = st.number_input("Units Owned", value=0.0, step=0.01 if market_type == "Crypto" else 1.0)
        avg_cost = st.number_input(f"Avg Purchase Price ({currency_symbol})", value=0.0)
        if qty > 0:
            portfolio = calculate_portfolio_metrics(df, qty, avg_cost)
            st.write(f"**P&L:** {currency_symbol}{portfolio['P&L']:.2f} ({portfolio['P&L %']:.2f}%)")
            st.write(f"**VaR (Risk):** {currency_symbol}{abs(portfolio['VaR (95%)']):.2f}")

    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["📊 Analysis", "🤖 AI Prediction", "⚖️ Benchmark", "🏢 Fundamentals", "📰 News Sentiment", "🧪 Backtesting", "📜 Raw Data"])

    with tab1:
        col1, col2 = st.columns([4, 1])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index, 
                open=df['Open'], 
                high=df['High'], 
                low=df['Low'], 
                close=df['Close'], 
                name="Price"
            ))
            # Add SMA overlays if available
            if 'SMA_20' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name="SMA 20", line=dict(color='orange', width=1)))
            if 'SMA_50' in df.columns:
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name="SMA 50", line=dict(color='cyan', width=1)))
            
            fig.update_layout(
                title=f"{ticker} Advanced Price Chart", 
                template="plotly_dark", 
                height=600,
                xaxis_rangeslider_visible=False,
                yaxis_title=f"Price ({currency_symbol})",
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🛠️ Technical Signals")
            last_rsi = df['RSI'].iloc[-1]
            st.info(f"**RSI Status:** {'Overbought' if last_rsi > 70 else 'Oversold' if last_rsi < 30 else 'Neutral'}")
            
            st.markdown("---")
            st.markdown("**Moving Averages**")
            if 'SMA_20' in df.columns and 'SMA_50' in df.columns:
                signal = "Bullish" if df['SMA_20'].iloc[-1] > df['SMA_50'].iloc[-1] else "Bearish"
                st.write(f"Trend: **{signal}**")
            
            st.markdown("**Day Range**")
            st.write(f"L: {currency_symbol}{df['Low'].iloc[-1]:.2f} - H: {currency_symbol}{df['High'].iloc[-1]:.2f}")

    with tab2:
        st.subheader("🤖 AI Price Forecasting (Random Forest)")
        days_to_pred = st.slider("Days to forecast", 1, 30, 7)
        predictions = predict_next_days(df, days_to_pred)
        
        fig_pred = go.Figure()
        fig_pred.add_trace(go.Scatter(x=df.index[-30:], y=df['Close'].iloc[-30:], name="Historical"))
        fig_pred.add_trace(go.Scatter(x=predictions.index, y=predictions.values, name="AI Prediction", line=dict(dash='dash', color='red')))
        fig_pred.update_layout(title="Prediction Model Output", template="plotly_dark")
        st.plotly_chart(fig_pred, width="stretch")
        st.warning("⚠️ Disclaimer: AI predictions are for educational purposes only. Do not base financial decisions solely on this model.")

    with tab3:
        st.subheader("⚖️ Performance vs Benchmark (S&P 500)")
        benchmark = fetch_benchmark_data("^GSPC", start_date, datetime.now())
        
        # Normalize to 100 for comparison
        norm_stock = (df['Close'] / df['Close'].iloc[0]) * 100
        norm_bench = (benchmark / benchmark.iloc[0]) * 100
        
        fig_bench = go.Figure()
        fig_bench.add_trace(go.Scatter(x=norm_stock.index, y=norm_stock, name=ticker))
        fig_bench.add_trace(go.Scatter(x=norm_bench.index, y=norm_bench, name="S&P 500"))
        fig_bench.update_layout(title="Relative Performance (Base 100)", template="plotly_dark")
        st.plotly_chart(fig_bench, width="stretch")

    with tab4:
        st.subheader(f"🏢 {ticker} Company Profile")
        info = fetch_ticker_info(ticker)
        
        if info and 'longBusinessSummary' in info:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown("**Business Summary**")
                st.write(info.get('longBusinessSummary', 'No summary available.'))
            
            with col2:
                st.markdown("**Key Information**")
                st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                st.write(f"**Industry:** {info.get('industry', 'N/A')}")
                st.write(f"**Full-time Employees:** {info.get('fullTimeEmployees', 'N/A'):,}")
                st.write(f"**Website:** [{info.get('website', 'N/A')}]({info.get('website', '#')})")

            st.divider()
            st.subheader("📊 Fundamental Metrics")
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            
            def format_val(val, prefix="", suffix=""):
                if val is None or val == "N/A": return "N/A"
                if abs(val) >= 1_000_000_000_000: return f"{prefix}{val/1_000_000_000_000:.2f}T{suffix}"
                if abs(val) >= 1_000_000_000: return f"{prefix}{val/1_000_000_000:.2f}B{suffix}"
                if abs(val) >= 1_000_000: return f"{prefix}{val/1_000_000:.2f}M{suffix}"
                return f"{prefix}{val:.2f}{suffix}"

            m_col1.metric("Market Cap", format_val(info.get('marketCap'), prefix=currency_symbol))
            m_col2.metric("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
            m_col3.metric("Div. Yield", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0.00%")
            m_col4.metric("EPS (TTM)", f"{currency_symbol}{info.get('trailingEps', 'N/A')}")
        else:
            st.info("Fundamental data is primarily available for Stocks. Some metrics may not be available for Crypto, Forex, or Commodities.")

    with tab5:
        st.subheader(f"📰 Latest News & Sentiment: {ticker}")
        news_list = fetch_ticker_news(ticker)
        
        if news_list:
            # Standardize news items structure
            standardized_news = []
            for n in news_list:
                content = n.get('content')
                if not isinstance(content, dict):
                    content = n  # Fallback to the item itself if 'content' is missing or not a dict
                
                item = {
                    'title': content.get('title', n.get('title', 'No Title')),
                    'publisher': content.get('provider', {}).get('displayName', n.get('publisher', 'Unknown')) if isinstance(content.get('provider'), dict) else n.get('publisher', 'Unknown'),
                    'link': content.get('clickThroughUrl', {}).get('url', n.get('link', '#')) if isinstance(content.get('clickThroughUrl'), dict) else n.get('link', '#')
                }
                standardized_news.append(item)

            # Aggregate Sentiment
            sentiments = [analyze_sentiment(n['title']) for n in standardized_news]
            bullish_count = sum(1 for s, e in sentiments if s == "Bullish")
            bearish_count = sum(1 for s, e in sentiments if s == "Bearish")
            neutral_count = sum(1 for s, e in sentiments if s == "Neutral")
            
            # Sentiment Summary
            s_col1, s_col2, s_col3 = st.columns(3)
            s_col1.metric("Bullish Headlines", bullish_count)
            s_col2.metric("Bearish Headlines", bearish_count)
            s_col3.metric("Neutral Headlines", neutral_count)
            
            st.divider()
            
            for i, news in enumerate(standardized_news):
                sentiment, emoji = sentiments[i]
                with st.expander(f"{emoji} {news['title']}"):
                    st.write(f"**Source:** {news['publisher']}")
                    st.write(f"**Sentiment:** {sentiment}")
                    st.write(f"**Link:** [Read Article]({news['link']})")
        else:
            st.info("No recent news found for this ticker.")

    with tab6:
        st.subheader("🧪 Strategy Backtesting")
        strategy = st.selectbox("Select Strategy", ["RSI Oversold", "SMA Crossover"])
        
        results = run_backtest(df, strategy)
        
        # Metrics Row
        b_col1, b_col2, b_col3, b_col4 = st.columns(4)
        b_col1.metric("Strategy Return", f"{results['Total Return (%)']:.2f}%")
        b_col2.metric("Market Return", f"{results['Market Return (%)']:.2f}%")
        b_col3.metric("Max Drawdown", f"{results['Max Drawdown (%)']:.2f}%")
        b_col4.metric("Win Rate", f"{results['Win Rate (%)']:.2f}%")
        
        # Plot Equity Curve
        fig_bt = go.Figure()
        fig_bt.add_trace(go.Scatter(x=results['Equity Curve'].index, y=results['Equity Curve']['Cum_Strategy_Return'], name="Strategy Equity"))
        fig_bt.add_trace(go.Scatter(x=results['Equity Curve'].index, y=results['Equity Curve']['Cum_Market_Return'], name="Market (Buy & Hold)", line=dict(dash='dash')))
        fig_bt.update_layout(title=f"Strategy Performance: {strategy}", template="plotly_dark", yaxis_title="Cumulative Return (Multiplier)")
        st.plotly_chart(fig_bt, width="stretch")

    with tab7:
        st.subheader(f"📜 Raw Historical Data: {ticker}")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
else:
    st.error("Ticker not found or API limit reached.")
