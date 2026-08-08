import pandas as pd
from src.database import get_engine
from src.data_generator import (
    generate_bond_universe,
    generate_yield_curve,
    generate_pricing_and_risk_data,
)


def run_pipeline():
  """Generates synthetic bond data, runs pricing and risk calculations,

  and populates the database tables required for the Streamlit dashboard.
  """
  print("1. Initializing database engine...")
  engine = get_engine()

  print("2. Generating synthetic bond universe and yield curve...")
  df_bonds = generate_bond_universe(n_bonds=50)
  df_curve = generate_yield_curve()

  print("3. Executing pricing models and risk analytics calculations...")
  df_pricing, df_risk = generate_pricing_and_risk_data(df_bonds, df_curve)

  print("4. Saving results to database tables...")
  df_bonds.to_sql("bonds", con=engine, if_exists="replace", index=False)
  df_pricing.to_sql(
      "bond_pricing_results", con=engine, if_exists="replace", index=False
  )
  df_risk.to_sql(
      "bond_risk_metrics", con=engine, if_exists="replace", index=False
  )

  print("Pipeline execution completed successfully!")


if __name__ == "__main__":
  run_pipeline()