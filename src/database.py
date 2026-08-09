import os
from sqlalchemy import create_engine

# Path for local SQLite database
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "bonds.db")
DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"


def get_engine():
  """Creates and returns a SQLAlchemy engine for SQLite."""
  return create_engine(DATABASE_URL, echo=False)