-- 1. Create the Database
CREATE DATABASE MarketWatchDB;
GO
USE MarketWatchDB;
GO

-- 2. Create the Table
-- We need a 'Log' table that keeps every single price tick history
CREATE TABLE LiveMarketData (
    DataID INT IDENTITY(1,1) PRIMARY KEY,
    Symbol VARCHAR(20),      -- e.g., 'GC=F' (Gold), 'GBPUSD=X'
    Price DECIMAL(18, 4),    -- The live rate
    TradeTimestamp DATETIME DEFAULT GETDATE() -- When we fetched it
);
GO

-- 3. Create a View for the "Latest" Price (For Power BI)
CREATE VIEW v_LatestRates AS
SELECT Symbol, Price, TradeTimestamp
FROM (
    SELECT *, 
           ROW_NUMBER() OVER(PARTITION BY Symbol ORDER BY TradeTimestamp DESC) as rn
    FROM LiveMarketData
) sub
WHERE rn = 1;
GO