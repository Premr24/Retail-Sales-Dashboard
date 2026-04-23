import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

def get_db_connection():
    username = 'root'
    password = os.getenv('DB_PASSWORD')
    host = 'localhost'
    database = 'retail_sales_db'
    return create_engine(f'mysql+pymysql://{username}:{password}@{host}/{database}')

def load_and_clean_data():
    # 1. Error Handling added here
    try:
        engine = get_db_connection()
        query = "SELECT * FROM sales"
        df = pd.read_sql(query, engine)
    except Exception as e:
        # Gracefully show an error in Streamlit instead of crashing
        st.error(f"Database Connection Failed. Please ensure MySQL is running. Error: {e}")
        st.stop()

    # Data Cleaning
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=True)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=True)
    df.dropna(subset=['Postal Code'], inplace=True)
    
    # 2. Drop duplicates added here
    df.drop_duplicates(inplace=True)

    return df