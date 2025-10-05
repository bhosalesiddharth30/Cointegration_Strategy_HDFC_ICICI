# Cointegration-Based Pairs Trading — HDFC Bank & ICICI Bank

This project implements a **statistical arbitrage (pairs trading)** strategy using **cointegration** between **HDFC Bank (HDFCBANK.NS)** and **ICICI Bank (ICICIBANK.NS)**.  
The strategy identifies periods when the two banks' stock prices diverge abnormally and profits from their **mean reversion**.

---

## 🚀 Overview

- Fetches 3–10 years of **daily adjusted closing prices** from Yahoo Finance.
- Performs **OLS linear regression** (HDFC = α + β·ICICI + ε) to estimate the hedge ratio β.
- Tests the **stationarity of the spread** using the **Augmented Dickey–Fuller (ADF)** test.
- Converts the spread into a **z-score** to identify over/under-valuation.
- Enters trades:
  - **z > +2** → Short spread (Short HDFC, Long β·ICICI)
  - **z < –2** → Long spread (Long HDFC, Short β·ICICI)
  - **|z| < 0.5** → Exit
- Evaluates performance with **Sharpe ratio**, **drawdown**, and **trade count**.

---

## 📊 Formulas

### 1. Regression
\[
HDFC_t = \alpha + \beta \cdot ICICI_t + \varepsilon_t
\]

### 2. Spread
\[
Spread_t = HDFC_t - \beta \cdot ICICI_t
\]

### 3. Z-score
\[
Z_t = \frac{Spread_t - \mu_{Spread,60}}{\sigma_{Spread,60}}
\]

### 4. Strategy Return
\[
R_t = Position_{t-1} \cdot \Delta Spread_t
\]

### 5. Sharpe Ratio
\[
Sharpe = \frac{E[R]}{\sigma_R} \cdot \sqrt{252}
\]

---

## 📈 Example Results (HDFC–ICICI 3-Year Daily Data)

| Metric | Value |
|--------|--------|
| Hedge ratio (β) | 1.12 |
| ADF p-value | 0.017 (<0.05 → stationary) |
| Trades executed | 16 |
| Sharpe ratio | 2.28 |
| Max drawdown | –2.5 |
| Win rate | 68% |

---

## ⚙️ How to Run

```bash
git clone https://github.com/yourusername/Cointegration-Strategy-HDFC-ICICI.git
cd Cointegration-Strategy-HDFC-ICICI
pip install -r requirements.txt
jupyter notebook cointegration.ipynb
