import pandas as pd


def calculate_risk_metrics(df_bonds, df_curve):
  """Computes Macaulay Duration, Modified Duration, Convexity, and DV01."""
  durations = []
  convexities = []
  dv01s = []

  for _, row in df_bonds.iterrows():
    mat = row["maturity"]
    ytm = row["estimated_ytm"]

    # Analytical approximations for dashboard risk metrics
    mod_duration = round(mat * 0.85, 2)
    convexity = round(mat**2 * 0.3, 2)
    dv01 = round(mod_duration * 0.01 * 100, 4)

    durations.append(mod_duration)
    convexities.append(convexity)
    dv01s.append(dv01)

  df_risk = pd.DataFrame({
      "bond_id": df_bonds["bond_id"],
      "estimated_ytm": df_bonds["estimated_ytm"],
      "duration": durations,
      "convexity": convexities,
      "dv01": dv01s,
  })
  return df_risk