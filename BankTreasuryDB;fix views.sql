USE BankTreasuryDB;
GO

-- Drop the view if it exists so we can recreate it cleanly
IF OBJECT_ID('v_TreasuryBoard', 'V') IS NOT NULL
    DROP VIEW v_TreasuryBoard;
GO

-- Create the Dashboard View
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