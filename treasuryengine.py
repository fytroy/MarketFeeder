import yfinance as yf
import pyodbc
import pandas as pd
from datetime import datetime
import time

# --- CONFIGURATION ---
# The 'r' before the string fixes the warning you saw earlier
SERVER = r'ROYSHP\FYT' 
DATABASE = 'BankTreasuryDB'
DRIVER = '{ODBC Driver 17 for SQL Server}'

# --- DATABASE CONNECTION ---
def get_db_connection():
    return pyodbc.connect(f'DRIVER={DRIVER};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')

def fetch_config():
    """Reads the asset list and bank margins from SQL Server"""
    conn = get_db_connection()
    query = "SELECT CurrencyCode, YahooTicker, BankSpreadMargin FROM Ref_Currencies"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def run_pricing_engine():
    print(f"\n--- 🌍 Treasury Engine Starting at {datetime.now().strftime('%H:%M:%S')} ---")
    
    # 1. Get the list of currencies
    try:
        config_df = fetch_config()
    except Exception as e:
        print(f"❌ Database Connection Failed: {e}")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    # 2. Loop through each currency
    for index, row in config_df.iterrows():
        symbol = row['CurrencyCode']
        ticker = row['YahooTicker']
        margin = float(row['BankSpreadMargin'])
        
        try:
            # A. Fetch Interbank Rate (Live Market)
            data = yf.Ticker(ticker)
            interbank_price = data.fast_info['last_price']
            
            # B. Apply Treasury Logic (The Bank's Profit)
            bank_buy = interbank_price * (1 - margin)
            bank_sell = interbank_price * (1 + margin)
            spread_profit = bank_sell - bank_buy

            # C. Push to SQL Ledger
            insert_query = """
            INSERT INTO Live_Market_Rates 
            (CurrencyCode, InterbankRate, BankBuyRate, BankSellRate, SpreadIncome)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(insert_query, (symbol, interbank_price, bank_buy, bank_sell, spread_profit))
            
            print(f"✅ {symbol}: Market {interbank_price:.4f} | Buy {bank_buy:.4f} | Sell {bank_sell:.4f}")
            
        except Exception as e:
            print(f"❌ Error fetching {symbol}: {e}")

    # 3. Save changes
    conn.commit()
    conn.close()
    print("--- 💾 Rates Published to Database ---")

# --- EXECUTION LOOP ---
if __name__ == "__main__":
    print("Starting Treasury Engine... (Press Ctrl+C to stop)")
    try:
        while True:
            run_pricing_engine()
            time.sleep(60) # Updates every 60 seconds
    except KeyboardInterrupt:
        print("Engine Stopped.")