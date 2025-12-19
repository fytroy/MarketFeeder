# Bank Treasury & Market Watch System

## Overview

This project is a comprehensive Bank Treasury System designed to track live market data, calculate bank treasury rates including margins, and store the data in a SQL Server database. It includes a data feeder for fetching raw market prices and a treasury engine for calculating client-facing rates. Additionally, a Power BI dashboard is provided for real-time visualization.

## Features

-   **Live Market Data Feed:** Fetches real-time prices for assets like Gold, Oil, Bitcoin, and major Forex pairs (e.g., GBP/USD) from Yahoo Finance.
-   **Treasury Pricing Engine:** Calculates Bank Buy and Sell rates based on configurable spreads/margins defined in the database.
-   **Data Persistence:** Stores all raw market data and calculated treasury rates in Microsoft SQL Server.
-   **Visualization:** Includes a Power BI dashboard (`dashboard.pbix`) connected to the database for monitoring rates and trends.

## Project Structure

-   `marketfeeder.py`: Fetches raw market data for tracked assets (Gold, Oil, BTC, GBP/USD) and pushes it to `MarketWatchDB`.
-   `treasuryengine.py`: The core logic that reads currency configurations, fetches live interbank rates, applies margins, and saves the calculated rates to `BankTreasuryDB`.
-   `Create MarketWatchDB.sql`: SQL script to set up the Market Watch database and tables.
-   `CREATE DATABASE BankTreasuryDB.sql`: SQL script to set up the Bank Treasury database, configuration tables, and live rate tables.
-   `BankTreasuryDB;fix views.sql`: SQL script to create or update the dashboard views.
-   `dashboard.pbix`: Power BI file for visualizing the data.

## Prerequisites

-   **Python 3.x**
-   **Microsoft SQL Server** (2019 or later recommended)
-   **ODBC Driver 17 for SQL Server**
-   **Power BI Desktop** (for viewing the dashboard)

## Installation & Setup

### 1. Database Setup

Execute the provided SQL scripts in your SQL Server Management Studio (SSMS) in the following order:

1.  Run `Create MarketWatchDB.sql` to create the `MarketWatchDB` database.
2.  Run `CREATE DATABASE BankTreasuryDB.sql` to create the `BankTreasuryDB` database and seed the initial configuration.
3.  Run `BankTreasuryDB;fix views.sql` to ensure the necessary views are created.

### 2. Python Environment Setup

1.  Clone this repository.
2.  Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

### 3. Configuration

Open `marketfeeder.py` and `treasuryengine.py` and update the database connection details to match your SQL Server environment:

```python
# Example in marketfeeder.py and treasuryengine.py
server = r'YOUR_SERVER_NAME'  # Update this to your SQL Server instance
database = 'MarketWatchDB'    # (or BankTreasuryDB)
driver = '{ODBC Driver 17 for SQL Server}'
```

Ensure that the `server` variable points to your correct SQL Server instance (e.g., `localhost`, `.\SQLEXPRESS`, or a remote server).

## Usage

### Running the Market Feeder

This script fetches raw market data for specific assets (Gold, Oil, BTC, GBP/USD) and logs it to `MarketWatchDB`.

```bash
python marketfeeder.py
```

### Running the Treasury Engine

This script acts as the pricing engine. It reads the currency configuration, fetches live rates, calculates the bank's buy/sell rates, and logs them to `BankTreasuryDB`.

```bash
python treasuryengine.py
```

Both scripts are designed to run continuously, updating data every 60 seconds.

## Dashboard

Open `dashboard.pbix` in Power BI Desktop. You may need to update the data source settings in Power BI to point to your local SQL Server instance and refresh the data to see the latest rates.
