import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import coint
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

# tickers
tickers = ["KOTAKBANK.NS", "BAJFINANCE.NS"]

# importing stock prices
data = yf.download(tickers, start="2018-01-01", end="2026-01-01", auto_adjust=True)["Close"]

data = data.dropna()

print(data.head())
print(data.tail())

# plot price series
data.plot(figsize=(10,5))
plt.title("KOTAKBANK vs BAJFINANCE")
plt.show()

# correlation
corr = data["KOTAKBANK.NS"].corr(data["BAJFINANCE.NS"])
print("The Correlation Coefficient is:", corr)

# cointegration test
score, pvalue, critical_values = coint(data["KOTAKBANK.NS"], data["BAJFINANCE.NS"])

print("cointegration pvalue is:", pvalue)


# regression for hedge ratio
X = data["BAJFINANCE.NS"]
Y = data["KOTAKBANK.NS"]

X = sm.add_constant(X)

model = sm.OLS(Y, X).fit()

hedge_ratio = model.params["BAJFINANCE.NS"]

print("Hedge Ratio:", hedge_ratio)

# spread calculation
data["Spread"] = data["KOTAKBANK.NS"] - hedge_ratio * data["BAJFINANCE.NS"]

data["Spread"].plot(figsize=(10,5))

plt.title("Spread Between KOTAKBANK and BAJFINANCE")
plt.xlabel("Date")
plt.ylabel("Spread Value")

plt.show()


# ADF test
result = adfuller(data["Spread"])

print("ADF Statistic:", result[0])
print("p-value:", result[1])


# Z-score calculation
window = 20

data["Spread_Mean"] = data["Spread"].rolling(window).mean()
data["Spread_Std"] = data["Spread"].rolling(window).std()

data["Zscore"] = (data["Spread"] - data["Spread_Mean"]) / data["Spread_Std"]

data["Spread_vol"] = data["Spread"].rolling(20).std()
vol_threshold = data["Spread_vol"].quantile(0.75)

# plot Z-score
data["Zscore"].plot(figsize=(10,5))

plt.axhline(1.96, color='red')
plt.axhline(-1.96, color='green')
plt.axhline(0, color='black')

plt.title("Z-Score of Spread")
plt.xlabel("Date")
plt.ylabel("Z-Score")

plt.show()


# trading signals
data["Position"] = 0
ENTRY = 2.2
EXIT = 1

data["Position"] = 0

data.loc[(data["Zscore"] > 2.2) & (data["Spread_vol"] < vol_threshold), "Position"] = -1
data.loc[(data["Zscore"] < -2.2) & (data["Spread_vol"] < vol_threshold), "Position"] = 1

data["Position"] = data["Position"].shift(1)


# stock returns
returns = data[["KOTAKBANK.NS","BAJFINANCE.NS"]].pct_change()


# strategy returns
data["Strategy_Return"] = data["Position"] * (
    returns["KOTAKBANK.NS"] - hedge_ratio * returns["BAJFINANCE.NS"]
)


# cumulative returns
data["Cumulative_Return"] = (1 + data["Strategy_Return"]).cumprod()


# equity curve
data["Cumulative_Return"].plot(figsize=(10,5))

plt.title("Pairs Trading Strategy Equity Curve")
plt.xlabel("Date")
plt.ylabel("Portfolio Value")

plt.show()


# Sharpe Ratio
sharpe = np.sqrt(252) * data["Strategy_Return"].mean() / data["Strategy_Return"].std()


# Max Drawdown
cum = data["Cumulative_Return"]

rolling_max = cum.cummax()

drawdown = (cum - rolling_max) / rolling_max

max_dd = drawdown.min()

print("Sharpe Ratio:", sharpe)
print("Max Drawdown:", max_dd)