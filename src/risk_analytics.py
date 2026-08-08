import numpy as np
import pandas as pd
from src.database import get_engine

def calculate_duration_and_convexity(maturity, coupon, freq, yield_to_maturity):
    """Calculates Macaulay Duration, Modified Duration, Convexity, and DV01."""
    n_periods = int(maturity * freq)
    coupon_payment = (1000.0 * coupon) / freq
    
    weighted_time_sum = 0.0
    weighted_convexity_sum = 0.0
    price_sum = 0.0
    
    for period in range(1, n_periods + 1):
        t = period / freq
        cf = coupon_payment
        if period == n_periods:
            cf += 1000.0
            
        discount_factor = (1 + yield_to_maturity / freq) ** (-period)
        pv_cf = cf * discount_factor
        
        weighted_time_sum += t * pv_cf
        weighted_convexity_sum += (t * (t + 1)) * pv_cf
        price_sum += pv_cf
        
    if price_sum <= 0:
        return 0.0, 0.0, 0.0, 0.0
        
    mac_dur = weighted_time_sum / price_sum
    mod_dur = mac_dur / (1 + yield_to_maturity / freq)
    
    # Convexity formula adjustment for payment frequency
    convexity = weighted_convexity_sum / (price_sum * ((1 + yield_to_maturity / freq) ** 2) * (freq ** 2))
    
    dv01 = (mod_dur * price_sum) / 10000.0
    
    return round(mac_dur, 2), round(mod_dur, 2), round(convexity, 2), round(dv01, 2)

def run_risk_analysis():
    engine = get_engine()
    df_bonds = pd.read_sql('bond_master', engine)
    
    analytics = []
    for _, bond in df_bonds.iterrows():
        maturity = bond['maturity_years']
        coupon = bond['coupon_rate']
        freq = bond['payment_frequency']
        market_price = bond['market_price']
        
        ytm = coupon + (1000.0 - market_price) / maturity / 1000.0
        ytm = max(0.01, ytm)
        
        mac_dur, mod_dur, convexity, dv01 = calculate_duration_and_convexity(maturity, coupon, freq, ytm)
        
        analytics.append({
            'bond_id': bond['bond_id'],
            'issuer_name': bond['issuer_name'],
            'market_price': market_price,
            'estimated_ytm': round(ytm, 4),
            'macaulay_duration': mac_dur,
            'modified_duration': mod_dur,
            'convexity': convexity,
            'dv01': dv01
        })
        
    df_risk = pd.DataFrame(analytics)
    df_risk.to_sql('bond_risk_metrics', engine, if_exists='replace', index=False)
    
    print("Risk analytics with Convexity executed successfully! Saved to 'bond_risk_metrics'.")
    print("\n--- Risk Metrics Sample ---")
    print(df_risk.head())

if __name__ == "__main__":
    run_risk_analysis()