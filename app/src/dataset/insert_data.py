import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv

class DataInserter:
    def __init__(self):
        load_dotenv()
        self.conn = None
        self.cur = None

    def read_csv(self, file_path):
        df = pd.read_csv(file_path, skiprows=2)
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        df = df.reset_index(drop=True)
        df.columns = ['id', 'code', 'company_name', 'industry', 'exchange', 'shares_outstanding']
        df['shares_outstanding'] = df['shares_outstanding']
        df['exchange'] = df['exchange'].str.upper()  # Uppercase the exchange column
        return df

    def connect_to_db(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        self.cur = self.conn.cursor()

    def create_table(self):
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id SERIAL PRIMARY KEY,
                code VARCHAR(30) UNIQUE NOT NULL,
                company_name VARCHAR(255) NOT NULL,
                industry VARCHAR(100),
                exchange VARCHAR(50),
                shares_outstanding VARCHAR(200)
            )
        """)

    def insert_data(self, df):
        insert_query = sql.SQL("""
            INSERT INTO companies (code, company_name, industry, exchange, shares_outstanding)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (code) DO UPDATE SET
                company_name = EXCLUDED.company_name,
                industry = EXCLUDED.industry,
                exchange = EXCLUDED.exchange,
                shares_outstanding = EXCLUDED.shares_outstanding
        """)

        for _, row in df.iterrows():
            print(row['code'], row['company_name'], row['industry'], row['exchange'], row['shares_outstanding'])
            self.cur.execute(insert_query, (row['code'], row['company_name'], row['industry'], row['exchange'], row['shares_outstanding']))

    def close_connection(self):
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    def run(self, file_path):
        df = self.read_csv(file_path)
        self.connect_to_db()
        self.create_table()
        self.insert_data(df)
        self.close_connection()
        print("Data has been successfully inserted into the PostgreSQL database.")
