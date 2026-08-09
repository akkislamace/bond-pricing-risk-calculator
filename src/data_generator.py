import numpy as np
import pandas as pd


def generate_bond_universe(n_bonds=50, seed=42):
  """Generates a synthetic universe of bonds with clean attributes."""
  np.random.seed(seed)

  bond_ids = [f"BOND_{i+1:03d}" for i in range(n_bonds)]
  coupons = np.round(np.random.uniform(0.02, 0.09, n_bonds), 4)
  maturities = np.round(np.random.uniform(1.0, 30.0, n_bonds), 1)
  face_values = [100.0] * n_bonds
  frequencies = [2] * n_bonds  # Semi-annual coupon payments

  df = pd.DataFrame({
      "bond_id": bond_ids,
      "coupon": coupons,
      "maturity": maturities,
      "face_value": face_values,
      "frequency": frequencies,
  })
  return df


def generate_yield_curve():
  """Generates a baseline benchmark yield curve across tenors."""
  tenors = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 20.0, 30.0]
  rates = [0.045, 0.047, 0.049, 0.050, 0.052, 0.054, 0.055, 0.057, 0.058]
  return pd.DataFrame({"tenor": tenors, "rate": rates})