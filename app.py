import streamlit as st
import pandas as pd
from src.database import get_engine

st.set_page_config(page_title="Bond Pricing & Risk Dashboard", layout="wide")

st.title("Fixed-Income Pricing & Risk Analytics Dashboard")
st.markdown("Analyze synthetic bond universes, evaluate theoretical mispricing, and compare risk metrics (Duration, Convexity, DV01).")

@st.cache_data
def load_data():
  engine = get_engine()
  try:
    df_pricing = pd.read_sql('bond_pricing_results', engine)
    df_risk = pd.read_sql('bond_risk_metrics', engine)
  except Exception:
    # If tables don't exist yet, run your main pipeline script to populate them automatically
    from main import run_pipeline

    run_pipeline()

    df_pricing = pd.read_sql('bond_pricing_results', engine)
    df_risk = pd.read_sql('bond_risk_metrics', engine)

  df_full = pd.merge(
      df_pricing, df_risk[['bond_id', 'estimated_ytm']], on='bond_id'
  )
  return df_full

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Bonds")
selected_issuers = st.sidebar.multiselect("Select Issuer(s)", options=df['issuer_name'].unique(), default=df['issuer_name'].unique())

filtered_df = df[df['issuer_name'].isin(selected_issuers)]

# Main View: Data Table
st.subheader("Bond Universe Overview")
st.dataframe(filtered_df, use_container_width=True)

# Comparison Section for up to 5 bonds
st.subheader("Side-by-Side Bond Comparison")
selected_bonds = st.multiselect("Select up to 5 Bonds to Compare", options=df['bond_id'].unique(), default=list(df['bond_id'].unique()[:3]))

if selected_bonds:
    comparison_df = df[df['bond_id'].isin(selected_bonds)]
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Market vs Model Price Comparison")
        chart_data = comparison_df.set_index('bond_id')[['market_price', 'model_price']]
        st.bar_chart(chart_data)
        
    with col2:
        st.markdown("#### Modified Duration & Convexity")
        risk_chart = comparison_df.set_index('bond_id')[['modified_duration', 'convexity']]
        st.bar_chart(risk_chart)
        
    st.markdown("#### Detailed Comparison Table")
    st.dataframe(comparison_df[['bond_id', 'issuer_name', 'coupon_rate', 'maturity_years', 'market_price', 'model_price', 'mispricing', 'modified_duration', 'convexity', 'dv01']], use_container_width=True)