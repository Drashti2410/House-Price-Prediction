import pandas as pd
from sqlalchemy import create_engine

DB_PATH = "data/housing.db"
engine = create_engine(f"sqlite:///{DB_PATH}")

def load_csv_to_db(csv_path="Housing.csv"):
    df = pd.read_csv(csv_path)
    df.to_sql("houses", engine, if_exists="replace", index=False)
    print(f"Loaded {len(df)} rows into {DB_PATH}")

def query_all():
    return pd.read_sql("SELECT * FROM houses", engine)

def query_filtered(min_price=None, max_bedrooms=None):
    query = "SELECT * FROM houses WHERE 1=1"
    if min_price:
        query += f" AND price >= {min_price}"
    if max_bedrooms:
        query += f" AND bedrooms <= {max_bedrooms}"
    return pd.read_sql(query, engine)

if __name__ == "__main__":
    load_csv_to_db()
