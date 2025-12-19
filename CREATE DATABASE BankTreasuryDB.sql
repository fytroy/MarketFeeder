CREATE DATABASE BankTreasuryDB;
GO
USE BankTreasuryDB;
GO

-- 1. Asset Reference Table (The "Config" Table)
-- This tells the engine what to fetch and what margin to charge.
CREATE TABLE Ref_Currencies (
    CurrencyCode VARCHAR(10) PRIMARY KEY, -- e.g., 'GBPUSD', 'USDKES'
    YahooTicker VARCHAR(20),              -- e.g., 'GBPUSD=X'
    AssetClass VARCHAR(20),               -- 'Forex', 'Commodity'
    BankSpreadMargin DECIMAL(10, 6)       -- e.g., 0.0050 (0.5% margin)
);

-- Seed with Tier 1 Assets
INSERT INTO Ref_Currencies (CurrencyCode, YahooTicker, AssetClass, BankSpreadMargin)
VALUES 
('EURUSD', 'EURUSD=X', 'Forex', 0.0020),  -- Low spread (Major Pair)
('GBPUSD', 'GBPUSD=X', 'Forex', 0.0025),
('USDKES', 'KES=X',    'Forex', 0.0150),  -- High spread (Exotic Pair)
('GOLD',   'GC=F',     'Commodity', 0.0080),
('OIL',    'CL=F',     'Commodity', 0.0080);

-- 2. Live Rates Table (The "Ticker")
-- This stores every single "tick" from the market.
CREATE TABLE Live_Market_Rates (
    RateID BIGINT IDENTITY(1,1) PRIMARY KEY,
    CurrencyCode VARCHAR(10),
    InterbankRate DECIMAL(18, 6), -- The raw Yahoo price
    BankBuyRate DECIMAL(18, 6),   -- We buy from customer at this (Lower)
    BankSellRate DECIMAL(18, 6),  -- We sell to customer at this (Higher)
    SpreadIncome DECIMAL(18, 6),  -- Potential profit per unit
    FetchTime DATETIME DEFAULT GETDATE()
);

-- 3. Live View for Dashboard (Shows only the latest tick per currency)
CREATE VIEW v_TreasuryBoard AS
SELECT 
    r.CurrencyCode,
    rc.AssetClass,
    r.InterbankRate,
    r.BankBuyRate,
    r.BankSellRate,
    r.FetchTime
FROM Live_Market_Rates r
JOIN Ref_Currencies rc ON r.CurrencyCode = rc.CurrencyCode
INNER JOIN (
    SELECT CurrencyCode, MAX(FetchTime) as MaxTime
    FROM Live_Market_Rates
    GROUP BY CurrencyCode
) latest ON r.CurrencyCode = latest.CurrencyCode AND r.FetchTime = latest.MaxTime;
GO