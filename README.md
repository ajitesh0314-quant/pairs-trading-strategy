# Pairs Trading Strategy (Z-Score + Hedge Ratio)

## Overview
This project implements a pairs trading strategy using two Indian stocks (KOTAKBANK and BAJFINANCE) based on mean reversion.

It uses statistical techniques like cointegration, hedge ratio estimation, and z-score normalization to identify trading opportunities.

## Methodology

### 1. Data Collection
- Historical price data from yFinance
- Time period: 2018–2026
- Stocks: KOTAKBANK.NS and BAJFINANCE.NS

### 2. Statistical Validation
- Correlation analysis
- Cointegration test (Engle-Granger)
- ADF test on spread to confirm stationarity

### 3. Hedge Ratio Estimation
- Linear regression (OLS) used to estimate hedge ratio
- Spread constructed as:
  Spread = Stock1 - (Hedge Ratio × Stock2)

### 4. Z-Score Calculation
- Rolling mean and standard deviation (window = 20)
- Z-score used to normalize spread

### 5. Trading Logic
- Enter short spread when Z-score > 2.2
- Enter long spread when Z-score < -2.2
- Volatility filter applied to avoid unstable periods
- Positions are shifted to avoid lookahead bias

### 6. Backtesting
- Strategy returns computed using spread returns
- Cumulative returns plotted as equity curve

## Performance Metrics
The Correlation Coefficient is: 0.922
cointegration pvalue is: 0.000299
Hedge Ratio: 0.231
ADF Statistic: -4.855
p-value: 4.2550
Sharpe Ratio: 0.652
Max Drawdown: -0.0797
## Key Insights
- Cointegration ensures mean-reverting behavior
- Hedge ratio improves spread accuracy vs simple subtraction
- Volatility filter helps reduce noisy trades
- Strategy performance depends heavily on parameter selection

## Tools Used
- Python
- Pandas
- NumPy
- yFinance
- Matplotlib
- Statsmodels

## Future Improvements
- Add transaction costs and slippage
- Optimize entry/exit thresholds
- Test multiple pairs
- Use rolling hedge ratio instead of static
