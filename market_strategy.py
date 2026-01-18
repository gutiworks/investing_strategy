import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import sys


year = sys.argv[1]
start_date = f"{year}-01-01"

end_year= sys.argv[2]
end_date = f"{end_year}-12-31"



# -------------------------
# TICKER
# -------------------------

history = yf.download(
    ["SPY", "^VIX"],
    interval="1d",
    start=start_date,
    end=end_date
)["Close"]



# -------------------------
# INDICATORS
# -------------------------

history["SPY_MA10"] = history["SPY"].rolling(window=30).mean()
history["VIX_MA10"] = history["^VIX"].rolling(window=10).mean()

history = history.round(2)


# -------------------------
# STRATEGY
# -------------------------

history["Signal"] = history.apply(
    lambda row: "BUY" if (row["^VIX"] < row["VIX_MA10"]) and (row["SPY"] > row["SPY_MA10"]) else "SELL",
    axis=1
)



# -------------------------
# PROFIT
# -------------------------

first_price = history["SPY"].iloc[0]
print(f"Starting Price: ${first_price}")

history["Daily_Diff"] = history["SPY"].diff()
history["Hold_Profit"] = history["Daily_Diff"].where(history["Signal"].shift(1) == "BUY", 0)

total_strategy_profit = history["Hold_Profit"].sum()
print(f"Total profit: ${total_strategy_profit:.2f}")

buy_and_hold_profit = history["SPY"].iloc[-1] - first_price
print(f"Total Profit (Just Hold): ${buy_and_hold_profit:.2f}")



# -------------------------
# RESULT
# -------------------------

#history["SPY"].plot()
#plt.show()

print(history)
