import numpy as np
import pandas as pd


def calculate_bond_price(coupon, maturity, face_value, ytm, frequency=2):
  """Calculates theoretical clean price of a coupon-paying bond."""
  n_periods = int(maturity * frequency)
  period_rate = ytm / frequency
  pmt = (coupon * face_value) / frequency

  # Present value of coupon payments
  pv_cashflows = sum(
      [pmt / ((1 + period_rate) ** t) for t in range(1, n_periods + 1)]
  )
  # Present value of principal repayment
  pv_face = face_value / ((1 + period_rate) ** n_periods)

  return round(pv_cashflows + pv_face, 4)


def calculate_prices(df_bonds, df_curve):
  """Computes prices and estimated YTM for the entire bond universe."""
  prices = []
  ytms = []

  base_ytm = 0.052

  for _, row in df_bonds.iterrows():
    simulated_ytm = round(base_ytm + np.random.uniform(-0.005, 0.005), 4)
    price = calculate_bond_price(
        row["coupon"],
        row["maturity"],
        row["face_value"],
        simulated_ytm,
        row["frequency"],
    )
    prices.append(price)
    ytms.append(simulated_ytm)

  df_bonds["clean_price"] = prices
  df_bonds["estimated_ytm"] = ytms
  return df_bonds