import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load the hidden variables from the .env file
load_dotenv()

def get_db_connection():
    """Establishes a connection to the MySQL database."""
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')
    
    db_url = f"mysql+pymysql://{user}:{password}@{host}/{db_name}"
    return create_engine(db_url)

def load_and_clean_data():
    """Pulls raw data from SQL and performs initial Pandas cleaning."""
    engine = get_db_connection()
    query = "SELECT * FROM sales"
    df = pd.read_sql(query, engine)
    
    # Standardize dates and handle missing values
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='%d/%m/%Y')
    df.dropna(subset=['Postal Code'], inplace=True)
    
    return df