import pandas as pd
from sqlalchemy import create_engine
from src.data_generator import generate_bond_universe, generate_yield_curve

# Replace 'YOUR_PASSWORD' with the master password you set in pgAdmin!
DB_URI = 'postgresql://postgres:Akshay16@localhost:5432/quant_db'

def get_engine():
    return create_engine(DB_URI)

def initialize_database():
    engine = get_engine()
    
    print("1. Generating 50 synthetic bonds and yield curve...")
    df_bonds = generate_bond_universe(n_bonds=50)
    df_curve = generate_yield_curve()
    
    print("2. Pushing datasets directly into PostgreSQL 'quant_db'...")
    df_bonds.to_sql('bond_master', engine, if_exists='replace', index=False)
    df_curve.to_sql('yield_curve', engine, if_exists='replace', index=False)
    
    print("Success! Database initialized and populated.")

if __name__ == "__main__":
    initialize_database()