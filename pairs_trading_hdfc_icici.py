"""
pairs_trading_hdfc_icici.py — Cointegration-Based Pairs Trading Strategy
Author: Siddharth Sunil Bhosale
"""

import pandas as pd, numpy as np, yfinance as yf
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
import matplotlib.pyplot as plt

# 1) Download data
df = yf.download(["HDFCBANK.NS", "ICICIBANK.NS"], period="3y", interval="1d")["Adj Close"].dropna()
hdfc, icici = df["HDFCBANK.NS"], df["ICICIBANK.NS"]

# 2) Hedge ratio (OLS)
X = sm.add_constant(icici)
ols = sm.OLS(hdfc, X).fit()
alpha, beta = ols.params["const"], ols.params["ICICIBANK.NS"]
print(f"Hedge ratio β = {beta:.3f}, Intercept α = {alpha:.3f}")

# 3) Spread
spread = hdfc - beta * icici

# 4) ADF test
adf_stat, pval, *_ = adfuller(spread.dropna())
print(f"ADF statistic = {adf_stat:.3f}, p-value = {pval:.4f}")
if pval < 0.05:
    print("✅ Reject H0: Spread is stationary → HDFC & ICICI are cointegrated")
else:
    print("❌ Fail to reject H0: Spread is not stationary")

# 5) Z-score
roll = 60
z = (spread - spread.rolling(roll).mean()) / spread.rolling(roll).std()
z = z.dropna()

# 6) Trading Logic
entry_hi, entry_lo, exit_th = 2.0, -2.0, 0.5
pos = pd.Series(0, index=z.index, dtype=float)
state = 0
for ts, val in z.items():
    if state == 0:
        if val > entry_hi:
            state = -1  # short spread (short HDFC, long ICICI)
        elif val < entry_lo:
            state = +1  # long spread (long HDFC, short ICICI)
    else:
        if abs(val) < exit_th:
            state = 0
    pos.loc[ts] = state

# 7) Backtest (simplified)
spread_ret = spread.diff().reindex(pos.index).fillna(0)
strategy_ret = pos.shift(1) * (-spread_ret)
cum = strategy_ret.cumsum()
sharpe = np.sqrt(252) * strategy_ret.mean() / strategy_ret.std()
max_dd = (cum - cum.cummax()).min()

# 8) Print Metrics
print(f"Trades executed: {(pos.diff().abs()==1).sum()}")
print(f"Sharpe ratio (annualized): {sharpe:.2f}")
print(f"Max drawdown: {max_dd:.2f}")

# 9) Plots
plt.figure(figsize=(8,4))
z.plot(title="Z-score of Spread (HDFC - β·ICICI)")
plt.axhline(2, ls="--"); plt.axhline(-2, ls="--"); plt.axhline(0, color="k")
plt.tight_layout(); plt.show()

plt.figure(figsize=(8,4))
cum.plot(title="Cumulative Strategy PnL (normalized units)")
plt.tight_layout(); plt.show()
