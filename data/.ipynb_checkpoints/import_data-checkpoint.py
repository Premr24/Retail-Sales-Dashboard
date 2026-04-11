import pandas as pd
from sqlalchemy import create_engine

# Read the dataset
df = pd.read_csv("train.csv")

# Setting up MySQL Connection
user = 'root'
password = 'prem2025csp'
host = 'localhost'
db_name = 'retail_sales_db'

db_url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
engine = create_engine(db_url)

df.to_sql(name='sales', con=engine, if_exists='replace', index=False)

print(f"Success! {len(df)} rows have been imported into MySQL.")