import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. Load environment variables from the .env file
load_dotenv()

# 2. Read the dataset
df = pd.read_csv("train.csv")

# 3. Setting up MySQL Connection securely
user = 'root'
# Fetching the password from your .env file instead of hardcoding it
password = os.getenv('DB_PASSWORD') 
host = 'localhost'
db_name = 'retail_sales_db'

# 4. Create the connection and import the data
db_url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
engine = create_engine(db_url)

df.to_sql(name='sales', con=engine, if_exists='replace', index=False)

print(f"Success! {len(df)} rows have been securely imported into MySQL.")