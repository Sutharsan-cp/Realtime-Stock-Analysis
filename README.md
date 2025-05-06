# 📈 Real-Time Stock Analysis Dashboard

A real-time stock analysis dashboard built with **Streamlit**, **Plotly**, and **Yahoo Finance**. This dashboard allows users to track stock performance, view technical indicators like Simple Moving Average (SMA) and Exponential Moving Average (EMA), analyze market volume, forecast future prices using linear regression, and compare stocks with major indices like S&P 500 and NASDAQ.

## Features

- **Real-Time Stock Data**: Fetch stock data from Yahoo Finance.
- **Candlestick Chart**: Display historical stock data in candlestick chart format.
- **Technical Indicators**: View SMA and EMA overlays on the price chart.
- **Forecasting**: Predict future stock prices based on historical data using linear regression.
- **Volume Analysis**: Visualize trading volume for the selected stock.
- **Correlation Matrix**: Visualize the correlation between stock open, high, low, close, and volume.
- **Price Alerts**: Set price alerts to be notified when a stock crosses a specified threshold.
- **Market Comparison**: Compare the stock performance with S&P 500 and NASDAQ indices.
- **Auto-Refresh**: The dashboard auto-refreshes the data at a specified interval.

## Requirements

- Python 3.x
- Streamlit
- yfinance
- plotly
- pandas
- numpy
- seaborn
- matplotlib
- scikit-learn

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Sutharsan-cp/stock-dashboard.git
2. Navigate to the project directory:
   ```bash
   cd stock-dashboard
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt


## Usage

1. To run the dashboard, simply execute the following command:
   ```bash
   streamlit run stock_dashboard.py
2. Open the provided URL in your web browser to interact with the stock dashboard.

## Features and Configuration

The dashboard includes a sidebar where you can configure the following:

- **📌 Stock Symbol (Ticker)**:  
  Enter the stock symbol (e.g., `AAPL`, `TSLA`, `MSFT`) to fetch its data.

- **🕒 Time Period**:  
  Select the time range for stock data analysis (e.g., `1mo`, `3mo`, `6mo`, `1y`, `2y`).

- **📉 SMA Window**:  
  Set the window size for the **Simple Moving Average (SMA)** overlay.

- **📈 EMA Window**:  
  Set the window size for the **Exponential Moving Average (EMA)** overlay.

- **🔮 Forecast Days**:  
  Specify how many days ahead you want to forecast the stock price using linear regression.

- **🚨 Price Alert**:  
  Set a price threshold to trigger an alert when the stock price crosses it.

- **🔁 Auto-Refresh**:  
  Configure the auto-refresh interval (in seconds) to update data in real-time.

 ## License
  This project is licensed under the MIT License. See the LICENSE file for more details.
