import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")
from plotly.subplots import make_subplots
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import os

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Stock Market Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: #00E5FF;
    text-align: center;
    font-size: 42px !important;
    font-weight: bold;
}

h2, h3 {
    color: #FFFFFF;
}

[data-testid="stMetricValue"] {
    color: #00FF9D;
    font-size: 28px;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

.stDataFrame {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# TITLE
# =========================

st.title("📈 AI Stock Market Analytics Dashboard")
def calculate_rsi(data, window=14):
    

    delta = data["Close"].diff()

    gain = delta.where(delta > 0, 0)

    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=window).mean()

    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    return rsi
def calculate_macd(data):
    

    exp1 = data["Close"].ewm(
        span=12,
        adjust=False
    ).mean()

    exp2 = data["Close"].ewm(
        span=26,
        adjust=False
    ).mean()

    macd = exp1 - exp2

    signal = macd.ewm(
        span=9,
        adjust=False
    ).mean()

    return macd, signal
def calculate_bollinger_bands(data):

    data["BB_MA"] = data["Close"].rolling(
        window=20
    ).mean()

    std = data["Close"].rolling(
        window=20
    ).std()

    data["Upper_Band"] = (
        data["BB_MA"] + (std * 2)
    )

    data["Lower_Band"] = (
        data["BB_MA"] - (std * 2)
    )

    return data
def load_stock(file_name):

    path = file_name

    temp_df = pd.read_csv(path)

    temp_df["Date"] = pd.to_datetime(temp_df["Date"])

    return temp_df
st.markdown("---")

# =========================
# LOAD DATA
# =========================

DATA_FOLDER = ""

stocks = {
    "Reliance": "reliance.csv",
    "TCS": "tcs.csv",
    "Infosys": "infosys.csv",
    "HDFC Bank": "hdfc_bank.csv",
    "ICICI Bank": "icici_bank.csv"
}
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio(
    "",
    [
        "🏠 Home",
        "📈 Analytics",
        "🤖 AI Prediction",
        "📊 Comparison",
        "📋 Reports",
        "ℹ️ About"
    ]
)

selected_stock = st.sidebar.selectbox(
    "Select Company",
    list(stocks.keys())
)


file_path = stocks[selected_stock]
)

df = pd.read_csv(file_path)

df["Date"] = pd.to_datetime(df["Date"])
df = calculate_bollinger_bands(df)



# =========================
# KPI CARDS
# =========================
if page == "🏠 Home":
    st.header("🏠 Dashboard Home")

elif page == "📈 Analytics":
    st.header("📈 Analytics")

elif page == "🤖 AI Prediction":
    st.header("🤖 AI Prediction")

elif page == "📊 Comparison":
    st.header("📊 Comparison")

elif page == "📋 Reports":
    st.header("📋 Reports")

elif page == "ℹ️ About":
    
    st.header("ℹ️ About Project")
    

latest_close = df["Close"].iloc[-1]
highest_close = df["Close"].max()
lowest_close = df["Close"].min()

col1, col2, col3 = st.columns(3)

col1.metric(
    "Current Price",
    f"₹ {latest_close:.2f}"
)

col2.metric(
    "Highest Price",
    f"₹ {highest_close:.2f}"
)

col3.metric(
    "Lowest Price",
    f"₹ {lowest_close:.2f}"
)

st.markdown("---")

# =========================
# CLOSING PRICE TREND
# =========================
st.subheader("MACD Indicator")

df["MACD"], df["Signal"] = calculate_macd(df)

macd_fig = go.Figure()

macd_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["MACD"],
        name="MACD"
    )
)

macd_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Signal"],
        name="Signal Line"
    )
)

macd_fig.update_layout(
    title="MACD Analysis",
    height=500
)

st.plotly_chart(
    macd_fig,
    use_container_width=True
)
st.subheader("Professional Candlestick Chart")
st.subheader("RSI Indicator")

df["RSI"] = calculate_rsi(df)

rsi_fig = px.line(
    df,
    x="Date",
    y="RSI",
    title="Relative Strength Index (RSI)"
)

rsi_fig.add_hline(y=70)
rsi_fig.add_hline(y=30)

st.plotly_chart(
    rsi_fig,
    use_container_width=True
)
candlestick_fig = go.Figure(
    data=[
        go.Candlestick(
            x=df["Date"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"]
        )
    ]
)

candlestick_fig.update_layout(
    title=f"{selected_stock} Candlestick Chart",
    height=600
)

st.plotly_chart(
    candlestick_fig,
    use_container_width=True
)

st.subheader("Closing Price Trend")

fig = px.line(
    df,
    x="Date",
    y="Close",
    title=f"{selected_stock} Closing Price"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown("---")
st.subheader("Correlation Heatmap")

heatmap_data = pd.DataFrame()

companies = {
    "Reliance": "reliance.csv",
    "TCS": "tcs.csv",
    "Infosys": "infosys.csv",
    "HDFC": "hdfc_bank.csv",
    "ICICI": "icici_bank.csv"
}

for company, file_name in companies.items():

    temp_df = load_stock(file_name)

    heatmap_data[company] = temp_df["Close"]

corr_matrix = heatmap_data.corr()

fig, ax = plt.subplots(figsize=(8, 6))

sns.heatmap(
    corr_matrix,
    annot=True,
    cmap="coolwarm",
    ax=ax
)

st.pyplot(fig)
st.markdown("---")
st.subheader("AI Price Prediction")

prediction_df = df.copy()

prediction_df = prediction_df[["Close"]]

prediction_df["Day"] = range(len(prediction_df))

X = prediction_df[["Day"]]

y = prediction_df["Close"]

model = LinearRegression()

model.fit(X, y)
train_predictions = model.predict(X)

accuracy = r2_score(
    y,
    train_predictions
)

accuracy_percent = accuracy * 100

next_day = [[len(prediction_df)]]

predicted_price = model.predict(next_day)[0]

st.metric(
    "Predicted Next Day Price",
    f"₹ {predicted_price:.2f}"
)
st.metric(
    "Model Accuracy",
    f"{accuracy_percent:.2f}%"
)
future_days = pd.DataFrame({
    "Day": range(
        len(prediction_df),
        len(prediction_df) + 7
    )
})

future_predictions = model.predict(
    future_days
)

forecast_df = pd.DataFrame({
    "Day": range(1, 8),
    "Predicted Price": future_predictions
})

forecast_fig = px.line(
    forecast_df,
    x="Day",
    y="Predicted Price",
    markers=True,
    title="7 Day Forecast"
)
st.markdown("---")

st.subheader("AI Recommendation Engine")

latest_rsi = df["RSI"].iloc[-1]

latest_macd = df["MACD"].iloc[-1]

latest_signal = df["Signal"].iloc[-1]

if latest_rsi < 70 and latest_macd > latest_signal:

    st.success("🟢 BUY Recommendation")

elif latest_rsi > 70:

    st.warning("🟡 HOLD Recommendation")

else:

    st.error("🔴 SELL Recommendation")

st.plotly_chart(
    forecast_fig,
    use_container_width=True
)

# =========================
# VOLUME ANALYSIS
# =========================

st.subheader("Volume Analysis")

volume_fig = px.bar(
    df,
    x="Date",
    y="Volume",
    title=f"{selected_stock} Trading Volume"
)

st.plotly_chart(
    volume_fig,
    use_container_width=True
)

# =========================
# MOVING AVERAGE
# =========================
st.subheader("Bollinger Bands Analysis")

bb_fig = go.Figure()

bb_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Close"],
        name="Close Price"
    )
)

bb_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Upper_Band"],
        name="Upper Band"
    )
)

bb_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["BB_MA"],
        name="Middle Band"
    )
)

bb_fig.add_trace(
    go.Scatter(
        x=df["Date"],
        y=df["Lower_Band"],
        name="Lower Band"
    )
)

bb_fig.update_layout(
    title="Bollinger Bands",
    height=600
)

st.plotly_chart(
    bb_fig,
    use_container_width=True
)
st.subheader("Moving Average Analysis")

if "MA20" in df.columns and "MA50" in df.columns:

    ma_fig = go.Figure()

    ma_fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Close"],
            name="Close"
        )
    )

    ma_fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA20"],
            name="MA20"
        )
    )

    ma_fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["MA50"],
            name="MA50"
        )
    )

    st.plotly_chart(
        ma_fig,
        use_container_width=True
    )

# =========================
# DAILY RETURNS
# =========================

if "Daily_Return" in df.columns:

    st.subheader("Daily Returns")

    return_fig = px.line(
        df,
        x="Date",
        y="Daily_Return"
    )

    st.plotly_chart(
        return_fig,
        use_container_width=True
    )

# =========================
# VOLATILITY
# =========================

if "Volatility" in df.columns:

    st.subheader("Volatility Analysis")

    vol_fig = px.line(
        df,
        x="Date",
        y="Volatility"
    )

    st.plotly_chart(
        vol_fig,
        use_container_width=True
    )

# =========================
# DATA TABLE
# =========================
st.markdown("---")

st.subheader("Download Report")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Dataset CSV",
    data=csv,
    file_name=f"{selected_stock}_report.csv",
    mime="text/csv"
)
st.markdown("---")

st.subheader("📰 Market Insights")

news_data = pd.DataFrame({
    "Headline": [
        "Reliance shows bullish momentum",
        "IT sector continues strong growth",
        "Banking stocks remain stable",
        "Market volatility decreases",
        "Investors show positive sentiment"
    ],
    "Category": [
        "Reliance",
        "Technology",
        "Banking",
        "Market",
        "Investment"
    ]
})

st.dataframe(
    news_data,
    use_container_width=True
)
st.subheader("Dataset Preview")

st.dataframe(
    df.tail(20),
    use_container_width=True
)
st.markdown("---")
st.subheader("Company Comparison Dashboard")

comparison_files = {
    "Reliance": "reliance.csv",
    "TCS": "tcs.csv",
    "Infosys": "infosys.csv"
}

comparison_fig = go.Figure()

for company, file_name in comparison_files.items():

    temp_df = load_stock(file_name)

    comparison_fig.add_trace(
        go.Scatter(
            x=temp_df["Date"],
            y=temp_df["Close"],
            mode="lines",
            name=company
        )
    )

comparison_fig.update_layout(
    title="Stock Price Comparison",
    height=600
)

st.plotly_chart(
    comparison_fig,
    use_container_width=True
)
