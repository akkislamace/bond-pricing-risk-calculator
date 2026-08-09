# Fixed-Income Pricing & Risk Analytics Dashboard

An interactive fixed-income analytics dashboard built with Python, Streamlit, and SQLAlchemy. This tool generates a synthetic bond universe, computes theoretical bond pricing using yield curve benchmarking, calculates core portfolio risk metrics (Duration, Convexity, DV01), and provides an interactive comparison tool.

## Features

- **Synthetic Bond Universe:** Generates clean bond datasets with variable maturities, coupon rates, and payment frequencies.
- **Yield Curve Pricing:** Computes theoretical clean prices and yield-to-maturity (YTM) metrics.
- **Risk Analytics Engine:** Calculates key fixed-income risk measures including Modified Duration, Convexity, and DV01.
- **Interactive 4-Bond Comparison:** Side-by-side analytical evaluation of user-selected bonds with dynamic metric cards.
- **Local Persistence:** Automated SQLite database synchronization via SQLAlchemy ORM.

## Project Architecture

```text
bond_pricing_calculator/
│
├── src/
│   ├── __init__.py
│   ├── database.py         # SQLite connection setup via SQLAlchemy
│   ├── data_generator.py   # Bond universe & yield curve generation
│   ├── pricing_model.py    # Bond pricing algorithms
│   └── risk_analytics.py   # Duration, Convexity, & DV01 analytics
│
├── app.py                  # Streamlit dashboard interface
├── requirements.txt        # Python dependency specifications
└── .gitignore              # Ignored local files and SQLite databases
