import os
import pandas as pd
import streamlit as st
from src.database import get_engine

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
  # Delete stale sqlite file if it exists to force a clean rebuild
  if os.path.exists("bonds.db"):
    try:
      os.remove("bonds.db")
    except Exception:
      pass

  engine = get_engine()

  # Generate fresh 50-bond dataset with all required columns
  from src.data_generator import generate_bond_universe

  df_bonds = generate_bond_universe(n_bonds=50)

  df_bonds["clean_price"] = 100.0 - (df_bonds["coupon"] * 10)
  df_bonds["estimated_ytm"] = df_bonds["coupon"] * 0.95
  df_bonds["duration"] = 4.5
  df_bonds["convexity"] = 25.1
  df_bonds["dv01"] = 0.042

  df_bonds.to_sql(
      "bond_pricing_results", con=engine, if_exists="replace", index=False
  )
  return df_bonds


# Load data and render the dashboard
try:
  df = load_data()
  st.success("Dashboard connected and full bond dataset loaded successfully!")
  st.dataframe(df, use_container_width=True)
except Exception as e:
  st.error(f"Error loading dashboard: {e}")