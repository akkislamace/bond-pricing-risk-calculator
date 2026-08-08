import streamlit as st
import pandas as pd
from src.database import get_engine
from src.data_generator import (
    generate_bond_universe,
    generate_yield_curve,
    generate_pricing_and_risk_data,
)

st.set_page_config(
    page_title="Fixed-Income Pricing & Risk Dashboard", layout="wide"
)

st.title("Fixed-Income Pricing & Risk Analytics Dashboard")
st.markdown(
    "Analyze synthetic bond universes, evaluate theoretical mispricing, and"
    " compare risk metrics (Duration, Convexity, DV01)."
)


@st.cache_data
def load_data():
  engine = get_engine()
  try:
    df_pricing = pd.read_sql("bond_pricing_results", engine)
    df_risk = pd.read_sql("bond_risk_metrics", engine)
  except Exception:
    # Automatically generate data and build tables if they don't exist yet
    df_bonds = generate_bond_universe(n_bonds=50)
    df_curve = generate_yield_curve()
    df_pricing, df_risk = generate_pricing_and_risk_data(df_bonds, df_curve)

    df_bonds.to_sql("bonds", con=engine, if_exists="replace", index=False)
    df_pricing.to_sql(
        "bond_pricing_results", con=engine, if_exists="replace", index=False
    )
    df_risk.to_sql(
        "bond_risk_metrics", con=engine, if_exists="replace", index=False
    )

    df_pricing = pd.read_sql("bond_pricing_results", engine)
    df_risk = pd.read_sql("bond_risk_metrics", engine)

  df_full = pd.merge(
      df_pricing, df_risk[["bond_id", "estimated_ytm"]], on="bond_id"
  )
  return df_full


# Load data into the app
try:
  df = load_data()
  st.success("Database connected and data loaded successfully!")
  st.dataframe(df.head())
except Exception as e:
  st.error(f"Error loading dashboard data: {e}")
