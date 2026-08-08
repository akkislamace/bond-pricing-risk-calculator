import numpy as np
import pandas as pd
from src.database import get_engine

def calculate_present_value(cash_flows, discount_rates):
    """Calculates the Present Value of a stream of cash flows given spot rates."""
    pv = sum(cf / ((1 + r) ** t) for cf, r, t in cash_flows)
    return round(pv, 2)

def price_bond_universe():
    engine = get_engine()
    
    # Load bonds and yield curve from PostgreSQL
    df_bonds = pd.read_sql('bond_master', engine)
    df_curve = pd.read_sql('yield_curve', engine)
    
    # Map tenors to spot rates for easy lookup
    spot_curve = dict(zip(df_curve['tenor_years'], df_curve['spot_rate']))
    
    prices = []
    for _, bond in df_bonds.iterrows():
        face = bond['face_value']
        coupon = bond['coupon_rate']
        freq = bond['payment_frequency']
        maturity = bond['maturity_years']
        
        # Construct cash flow schedule
        n_periods = int(maturity * freq)
        coupon_payment = (face * coupon) / freq
        
        cash_flows = []
        for period in range(1, n_periods + 1):
            t = period / freq
            cf = coupon_payment
            if period == n_periods:
                cf += face # Add principal return at maturity
                
            # Find the closest spot rate from our yield curve
            available_tenors = list(spot_curve.keys())
            closest_tenor = min(available_tenors, key=lambda x: abs(x - t))
            rate = spot_curve[closest_tenor]
            
            cash_flows.append((cf, rate, t))
            
        # Calculate theoretical model price
        model_price = calculate_present_value(cash_flows, spot_curve)
        market_price = bond['market_price']
        mispricing = round(model_price - market_price, 2)
        
        prices.append({
            'bond_id': bond['bond_id'],
            'issuer_name': bond['issuer_name'],
            'coupon_rate': coupon,
            'maturity_years': maturity,
            'market_price': market_price,
            'model_price': model_price,
            'mispricing': mispricing
        })
        
    df_results = pd.DataFrame(prices)
    
    # Push pricing results back to PostgreSQL as a new table!
    df_results.to_sql('bond_pricing_results', engine, if_exists='replace', index=False)
    print("Pricing engine executed successfully! Results saved to 'bond_pricing_results' table.")
    print("\n--- Top 5 Priced Bonds ---")
    print(df_results.head())

if __name__ == "__main__":
    price_bond_universe()