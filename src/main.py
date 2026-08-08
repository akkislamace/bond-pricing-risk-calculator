from src.database import initialize_database
from src.pricing_model import price_bond_universe
from src.risk_analytics import run_risk_analysis

if __name__ == "__main__":
    print("=== STARTING BOND PRICING & RISK PIPELINE ===")
    
    # Step 1: Initialize database & load datasets
    initialize_database()
    
    print("\n-------------------------------------------")
    
    # Step 2: Execute pricing model
    price_bond_universe()
    
    print("\n-------------------------------------------")
    
    # Step 3: Run risk analytics
    run_risk_analysis()
    
    print("\n=== PIPELINE EXECUTION COMPLETE ===")