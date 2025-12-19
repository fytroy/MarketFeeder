import yfinance as yf
import pyodbc
from datetime import datetime
import time

# --- CONFIGURATION ---
# 1. Your Server Details
server = r'ROYSHP\FYT'  # <--- CHECK THIS in your SSMS Connect box
database = 'MarketWatchDB'
driver = '{ODBC Driver 17 for SQL Server}' # Standard for SQL 2019/2022

# 2. What assets do you want to track?
# Symbols: Gold (GC=F), Oil (CL=F), Bitcoin (BTC-USD), GBP/USD (GBPUSD=X)
tickers_list = ['GC=F', 'CL=F', 'BTC-USD', 'GBPUSD=X']

# --- DATABASE CONNECTION FUNCTION ---
def get_db_connection():
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(conn_str)

# --- ETL PROCESS ---
def fetch_and_load():
    print(f"--- Fetching Data at {datetime.now()} ---")
    
    # 1. Connect to DB
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
    except Exception as e:
        print(f"Error connecting to SQL: {e}")
        return

    # 2. Loop through tickers
    for ticker in tickers_list:
        try:
            # Fetch Data from Yahoo
            stock = yf.Ticker(ticker)
            # 'fast_info' is faster than 'history' for live current price
            current_price = stock.fast_info['last_price']
            
            # 3. Insert into SQL
            query = "INSERT INTO LiveMarketData (Symbol, Price) VALUES (?, ?)"
            cursor.execute(query, (ticker, current_price))
            print(f"   Saved {ticker}: {current_price}")
            
        except Exception as e:
            print(f"   Failed to fetch {ticker}: {e}")

    # 4. Commit and Close
    conn.commit()
    cursor.close()
    conn.close()
    print("--- Data Push Complete ---\n")

# --- RUN LOOP (Runs every 60 seconds) ---
if __name__ == "__main__":
    print("Starting Market Feeder... (Press Ctrl+C to stop)")
    while True:
        fetch_and_load()
        time.sleep(60) # Wait 60 seconds before next run