import pandas as pd
import streamlit as st
from src.pricing_model import calculate_prices
from src.risk_analytics import calculate_risk_metrics
from src.data_generator import generate_bond_universe, generate_yield_curve
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
  engine = get_engine()
  try:
    # Try reading the complete tables from the SQLite database
    df_pricing = pd.read_sql("bond_pricing_results", engine)
    df_risk = pd.read_sql("bond_risk_metrics", engine)
    df_full = pd.merge(
        df_pricing, df_risk[["bond_id", "estimated_ytm"]], on="bond_id"
    )
    return df_full
  except Exception:
    # If tables don't exist yet, generate the full dataset of 50 synthetic bonds on the fly
    df_bonds = generate_bond_universe(n_bonds=50)
    df_curve = generate_yield_curve()

    df_pricing = calculate_prices(df_bonds, df_curve)
    df_risk = calculate_risk_metrics(df_bonds, df_curve)

    # Save them to the SQLite database tables
    df_pricing.to_sql(
        "bond_pricing_results", con=engine, if_exists="replace", index=False
    )
    df_risk.to_sql(
        "bond_risk_metrics", con=engine, if_exists="replace", index=False
    )

    df_full = pd.merge(
        df_pricing, df_risk[["bond_id", "estimated_ytm"]], on="bond_id"
    )
    return df_full


# Load data and render the dashboard
try:
  df = load_data()
  st.success("Dashboard connected and full bond dataset loaded successfully!")
  st.dataframe(df, use_container_width=True)
except Exception as e:
  st.error(f"Error loading dashboard: {e}")