import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time

# Streamlit Page Configuration
st.set_page_config(page_title="📈 Stock Dashboard", layout="wide")
st.title("📊 Real-Time Stock Analysis Dashboard")

# Sidebar Inputs
st.sidebar.header("Stock Settings")
ticker = st.sidebar.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, MSFT)", "AAPL").upper()
time_period = st.sidebar.selectbox("Select Time Period", ["1mo", "3mo", "6mo", "1y", "2y"])
sma_days = st.sidebar.slider("SMA Window", 5, 50, 20)
ema_days = st.sidebar.slider("EMA Window", 5, 50, 20)
forecast_days = st.sidebar.slider("Forecast Days", 5, 30, 10)
alert_price = st.sidebar.number_input("Set Price Alert ($)", value=0.0, step=0.1)
refresh_rate = st.sidebar.slider("Auto-Refresh (seconds)", 5, 60, 10)

# Fetch Stock Data
@st.cache_data(ttl=refresh_rate)
def get_stock_data(ticker, time_period):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period=time_period)
        if data.empty:
            return None, f"⚠️ No data found for {ticker}. Check the ticker symbol."
        return data, None
    except Exception as e:
        return None, f"❌ Error fetching {ticker}: {e}"

# Correlation Matrix
def plot_correlation_matrix(stock_data):
    corr = stock_data[['Open', 'High', 'Low', 'Close', 'Volume']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

# Forecasting Future Prices
def forecast_prices(stock_data, forecast_days):
    df = stock_data[["Close"]].reset_index()
    df["Days"] = (df["Date"] - df["Date"].min()).dt.days

    X = df[["Days"]]
    y = df["Close"]

    model = LinearRegression()
    model.fit(X, y)

    future_days = np.array(range(df["Days"].max() + 1, df["Days"].max() + forecast_days + 1)).reshape(-1, 1)
    future_prices = model.predict(future_days)

    future_dates = pd.date_range(df["Date"].max(), periods=forecast_days + 1, freq="D")[1:]

    forecast_df = pd.DataFrame({"Date": future_dates, "Forecasted Price": future_prices})
    return forecast_df

# Fetch and Process Data
stock_data, error = get_stock_data(ticker, time_period)
if stock_data is None:
    st.warning(error)
else:
    last_price = stock_data["Close"].iloc[-1]
    prev_price = stock_data["Close"].iloc[-2]
    change = last_price - prev_price
    pct_change = (change / prev_price) * 100
    st.metric(label=f"{ticker} Price", value=f"${last_price:.2f}", delta=f"{change:.2f} ({pct_change:.2f}%)")

    # Price Alert System
    if alert_price > 0:
        if last_price >= alert_price:
            st.warning(f"🚨 **ALERT:** {ticker} has crossed ${alert_price}!")

    # Compute Technical Indicators
    stock_data["SMA"] = stock_data["Close"].rolling(window=sma_days, min_periods=1).mean()
    stock_data["EMA"] = stock_data["Close"].ewm(span=ema_days, adjust=False).mean()

    

    # Plot Stock Chart
    st.subheader("📈 Stock Price & Indicators")
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=stock_data.index, open=stock_data["Open"], high=stock_data["High"], low=stock_data["Low"], close=stock_data["Close"], name="Candlestick"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["SMA"], mode="lines", name=f"{sma_days}-Day SMA"))
    fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data["EMA"], mode="lines", name=f"{ema_days}-Day EMA"))
    fig.update_layout(title=f"{ticker} Stock Analysis", xaxis_title="Date", yaxis_title="Price", template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

    # Plot Correlation Matrix
    st.subheader("📌 Correlation Matrix")
    plot_correlation_matrix(stock_data)

    # Volume Analysis
    st.subheader("📊 Volume Analysis")
    fig_volume = go.Figure()
    fig_volume.add_trace(go.Bar(x=stock_data.index, y=stock_data["Volume"], name="Volume"))
    fig_volume.update_layout(title=f"{ticker} Trading Volume", xaxis_title="Date", yaxis_title="Volume", template="plotly_dark")
    st.plotly_chart(fig_volume, use_container_width=True)

    # Forecasting Future Prices
    st.subheader("🔮 Stock Price Forecast")
    forecast_df = forecast_prices(stock_data, forecast_days)
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=stock_data.index, y=stock_data["Close"], mode="lines", name="Historical Prices"))
    fig_forecast.add_trace(go.Scatter(x=forecast_df["Date"], y=forecast_df["Forecasted Price"], mode="lines", name="Forecasted Prices", line=dict(dash="dot")))
    fig_forecast.update_layout(title=f"{ticker} Forecast for Next {forecast_days} Days", xaxis_title="Date", yaxis_title="Price", template="plotly_dark")
    st.plotly_chart(fig_forecast, use_container_width=True)

    # Market Comparison
    st.subheader("📊 Market Comparison")
    sp500 = get_stock_data("^GSPC", time_period)[0]
    nasdaq = get_stock_data("^IXIC", time_period)[0]
    if sp500 is not None and nasdaq is not None:
        st.line_chart({"Stock": stock_data['Close'], "S&P 500": sp500['Close'], "NASDAQ": nasdaq['Close']})
    
    # Auto-Refresh
    time.sleep(refresh_rate)
    st.rerun()
