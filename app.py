import pandas as pd
import streamlit as st
from src.data_generator import generate_bond_universe, generate_yield_curve
from src.database import get_engine
from src.pricing_model import calculate_prices
from src.risk_analytics import calculate_risk_metrics

st.set_page_config(
    page_title="Fixed-Income Pricing & Risk Dashboard", layout="wide"
)

st.title("Fixed-Income Pricing & Risk Analytics Dashboard")
st.markdown(
    "Analyze synthetic bond universes, evaluate theoretical pricing, and"
    " compare risk metrics across selected bonds."
)


@st.cache_data
def load_and_process_data():
  engine = get_engine()

  # Generate fresh data components
  df_bonds = generate_bond_universe(n_bonds=50)
  df_curve = generate_yield_curve()

  df_pricing = calculate_prices(df_bonds, df_curve)
  df_risk = calculate_risk_metrics(df_bonds, df_curve)

  # Merge results for display
  df_full = pd.merge(
      df_pricing,
      df_risk[["bond_id", "duration", "convexity", "dv01"]],
      on="bond_id",
  )

  # Save to local SQLite database tables
  df_full.to_sql(
      "bond_pricing_results", con=engine, if_exists="replace", index=False
  )
  df_risk.to_sql(
      "bond_risk_metrics", con=engine, if_exists="replace", index=False
  )

  return df_full


try:
  df = load_and_process_data()
  st.success("Local database connected and full analytics dataset loaded!")

  # Summary Metric Cards (Top Banner)
  m1, m2, m3, m4 = st.columns(4)
  m1.metric("Total Universe", f"{len(df)} Bonds")
  m2.metric("Avg Coupon Rate", f"{df['coupon'].mean():.2%}")
  m3.metric("Avg Yield (YTM)", f"{df['estimated_ytm'].mean():.2%}")
  m4.metric("Avg Duration", f"{df['duration'].mean():.2f} Yrs")

  st.divider()

  # ---------------------------------------------------------
  # 4-BOND COMPARISON SECTION
  # ---------------------------------------------------------
  st.subheader("Interactive Bond Comparison Tool")
  st.markdown("Select up to **4 bonds** to compare their risk and pricing side-by-side:")

  # Pre-select first 4 bonds by default
  default_bonds = list(df["bond_id"].head(4))

  selected_bonds = st.multiselect(
      "Choose Bonds for Comparison:",
      options=list(df["bond_id"]),
      default=default_bonds,
      max_selections=4,
  )

  if selected_bonds:
    df_compared = df[df["bond_id"].isin(selected_bonds)].copy()

    # Re-order columns for clean side-by-side view
    comparison_view = df_compared[[
        "bond_id",
        "coupon",
        "maturity",
        "clean_price",
        "estimated_ytm",
        "duration",
        "convexity",
        "dv01",
    ]].reset_index(drop=True)

    st.dataframe(comparison_view, use_container_width=True)

    # Visual Metric Cards for Selected Comparison
    st.markdown("#### Comparison Summary")
    c1, c2, c3, c4 = st.columns(4)
    for idx, b_id in enumerate(selected_bonds):
      b_row = df[df["bond_id"] == b_id].iloc[0]
      cols = [c1, c2, c3, c4]
      with cols[idx]:
        st.info(f"**{b_id}**")
        st.write(f"**Price:** ${b_row['clean_price']:.2f}")
        st.write(f"**YTM:** {b_row['estimated_ytm']:.2%}")
        st.write(f"**Duration:** {b_row['duration']} yrs")
        st.write(f"**DV01:** {b_row['dv01']}")
  else:
    st.warning("Please select at least one bond to view comparison analytics.")

  st.divider()

  # Complete Data Table
  st.subheader("Complete Bond Universe Master Table")
  st.dataframe(df, use_container_width=True)

except Exception as e:
  st.error(f"Error loading dashboard: {e}")