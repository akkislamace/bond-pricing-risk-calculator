import pandas as pd
import numpy as np

def generate_bond_universe(n_bonds=50, seed=42):
    """Generates a realistic synthetic universe of government and corporate bonds."""
    np.random.seed(seed)
    
    issuers = [
        'Government of India', 'HDFC Bank', 'Reliance Industries', 
        'State Bank of India', 'ICICI Bank', 'TATA Steel', 'L&T Finance'
    ]
    ratings = ['AAA', 'AA+', 'AA', 'A+']
    maturities = [1, 2, 3, 5, 7, 10, 15, 30]
    frequencies = [1, 2] # 1 = Annual, 2 = Semi-Annual
    
    bonds = []
    for i in range(1, n_bonds + 1):
        bond_id = f"BOND_{i:03d}"
        issuer = np.random.choice(issuers)
        face_value = 1000.0
        coupon_rate = round(np.random.uniform(0.055, 0.095), 4) # 5.5% to 9.5%
        frequency = int(np.random.choice(frequencies))
        maturity_years = int(np.random.choice(maturities))
        rating = np.random.choice(ratings)
        market_price = round(face_value * np.random.uniform(0.92, 1.08), 2)
        
        bonds.append({
            'bond_id': bond_id,
            'issuer_name': issuer,
            'face_value': face_value,
            'coupon_rate': coupon_rate,
            'payment_frequency': frequency,
            'maturity_years': maturity_years,
            'credit_rating': rating,
            'market_price': market_price
        })
        
    return pd.DataFrame(bonds)

def generate_yield_curve():
    """Generates a benchmark zero-coupon spot yield curve."""
    tenors = [0.5, 1.0, 2.0, 3.0, 5.0, 7.0, 10.0, 15.0, 30.0]
    spot_rates = [0.0620, 0.0635, 0.0650, 0.0670, 0.0695, 0.0715, 0.0730, 0.0745, 0.0760]
    
    return pd.DataFrame({
        'tenor_years': tenors,
        'spot_rate': spot_rates
    })

if __name__ == "__main__":
    df_bonds = generate_bond_universe()
    df_curve = generate_yield_curve()
    print("--- Generated Bond Universe Sample ---")
    print(df_bonds.head())
    print("\n--- Generated Spot Yield Curve ---")
    print(df_curve)