# 📈 Professional Stock Market Data Analysis Platform

A high-performance, interactive dashboard for financial market analysis built with Python, Streamlit, and Plotly. This platform provides deep market intelligence through technical analysis, AI-driven forecasting, and portfolio risk assessment.

## 🚀 Key Features

- **🌍 Multi-Market Expansion:** Full support for diverse financial assets:
  - **Stocks:** Global equities (e.g., AAPL, TSLA).
  - **Crypto:** Digital assets (e.g., BTC-USD, ETH-USD).
  - **Forex:** Currency pairs (e.g., EURUSD=X, GBPUSD=X).
  - **Commodities:** Precious metals and energy (e.g., Gold GC=F, Oil CL=F).
- **🧪 Strategy Backtesting:** Simulate trading strategies (RSI, SMA Crossover) against historical data to calculate win rates, total returns, and maximum drawdowns.
- **🏢 Fundamental Analysis:** Deep dive into company health with P/E ratios, Market Cap, Dividend Yield, and comprehensive business summaries.
- **📰 News Sentiment Analysis:** Real-time news feed integration with an AI-powered sentiment engine that classifies headlines as Bullish, Bearish, or Neutral.
- **🤖 AI Price Forecasting:** Integrated Random Forest machine learning model to predict future price trends based on historical patterns.
- **📊 Advanced Technical Analysis:** Automated calculation of professional indicators:
  - **Trend:** SMA (20, 50), MACD.
  - **Momentum:** RSI (Relative Strength Index).
  - **Volatility:** Bollinger Bands.
- **💼 Portfolio Management:** Track your holdings with real-time P&L calculation and advanced risk metrics like **Value at Risk (VaR 95%)**.
- **⚖️ Benchmark Comparison:** Compare stock performance against major indices like the S&P 500 (`^GSPC`) using normalized base-100 analysis.
- **💾 Local Data Caching:** Integrated SQLite database to cache market data, reducing API calls and improving performance.
- **📈 Interactive Visualizations:** Professional-grade candlestick charts and forecasting plots powered by Plotly.
- **📱 Responsive UI:** Modern, dark-themed dashboard with intuitive tabbed navigation.

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Machine Learning:** Scikit-learn (Random Forest)
- **Visualization:** Plotly, Seaborn, Matplotlib
- **Data Engine:** Pandas, yFinance, SQLAlchemy (SQLite)
- **Analytics:** Pandas-TA (Technical Analysis Library)

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/antoi/stock-market-data-analysis.git
   cd stock-market-data-analysis
   ```

2. **Set up Virtual Environment (Recommended):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```