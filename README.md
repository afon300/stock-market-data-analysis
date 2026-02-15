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

## 🌐 Deployment (Docker & SSL)

The platform is configured for automated deployment with **Nginx** and **Let's Encrypt** SSL.

### 1. DNS Setup 
In your Namecheap dashboard, add an **A Record**:
- **Host:** `@`
- **Value:** `Your-Server-IP`
- **TTL:** Automatic

### 2. Launch with Docker
On your server, run:
```bash
docker-compose up -d
```
The application will be available securely at `https://fourneyron.digital`.

## 📂 Project Structure

- `app.py`: Main Streamlit application with multi-tab interface.
- `src/`: Core logic modules.
  - `data_loader.py`: API integration, robust error handling, and SQLite caching.
  - `indicators.py`: Technical analysis (RSI, MACD, BBands) and portfolio risk metrics.
  - `models.py`: AI forecasting engine using Random Forest.
  - `sentiment.py`: AI-powered text analysis for financial news.
  - `backtest.py`: Engine for simulating trading strategies.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---
*⚠️ **Disclaimer:** This platform is for educational and research purposes only. AI predictions and financial metrics are not financial advice. Past performance is not indicative of future results.*
