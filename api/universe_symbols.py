"""
Broad NSE price universe for the central-store `quotes.json`.

This is a curated list of liquid NSE symbols (~Nifty 200 + popular mid/small
caps that users commonly hold). It exists so the daily job can publish an
end-of-day price map for a wide set of stocks, and the app's portfolio reads
LTPs from that central store instead of every client hitting a price API.

Symbols are plain NSE tickers (no ".NS"); the fetcher appends the suffix.
Unknown/renamed symbols simply fail the fetch and are skipped — safe to over-
include. Keep it sorted and de-duplicated.
"""

# ── Core large-caps (also the scored set) ──────────────────────────────────
UNIVERSE = [
    # Nifty 50 heavyweights
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "WIPRO", "HCLTECH",
    "BAJFINANCE", "TITAN", "SUNPHARMA", "MARUTI", "BHARTIARTL", "AXISBANK",
    "KOTAKBANK", "LT", "SBIN", "NTPC", "APOLLOHOSP", "TRENT", "LTIM",
    "ADANIPORTS", "HINDUNILVR", "ITC", "BAJAJFINSV", "TATAMOTORS", "TATASTEEL",
    "ASIANPAINT", "DRREDDY", "CIPLA", "EICHERMOT", "HEROMOTOCO", "BAJAJ-AUTO",
    "BRITANNIA", "NESTLEIND", "POWERGRID", "ONGC", "HAL", "BEL", "PERSISTENT",
    "COFORGE", "POLYCAB", "DIXON", "PFC", "RECLTD", "TATACONSUM", "INDUSINDBK",
    "HINDALCO", "JSWSTEEL", "DIVISLAB", "COALINDIA",

    # Banks / NBFC / financials
    "BANKBARODA", "PNB", "CANBK", "IDFCFIRSTB", "FEDERALBNK", "AUBANK",
    "BANDHANBNK", "CHOLAFIN", "SHRIRAMFIN", "MUTHOOTFIN", "SBICARD",
    "HDFCLIFE", "SBILIFE", "ICICIPRULI", "ICICIGI", "LICHSGFIN", "IDFC",
    "M&MFIN", "PEL", "LICI", "IRFC", "POONAWALLA",

    # IT / tech / new-age
    "TECHM", "MPHASIS", "LTTS", "OFSS", "TATAELXSI", "KPITTECH", "ZOMATO",
    "ETERNAL", "PAYTM", "NYKAA", "POLICYBZR", "NAUKRI", "IRCTC", "INDIAMART",
    "AFFLE", "ROUTE", "CYIENT", "ZENSARTECH", "BSOFT",

    # Auto / ancillaries
    "M&M", "TVSMOTOR", "ASHOKLEY", "BHARATFORG", "MOTHERSON", "BOSCHLTD",
    "BALKRISIND", "MRF", "APOLLOTYRE", "EXIDEIND", "TIINDIA", "SONACOMS",
    "UNOMINDA", "ENDURANCE",

    # Pharma / healthcare
    "AUROPHARMA", "LUPIN", "BIOCON", "TORNTPHARM", "ALKEM", "ZYDUSLIFE",
    "GLENMARK", "IPCALAB", "LAURUSLABS", "MANKIND", "MAXHEALTH", "FORTIS",
    "SYNGENE", "GLAND", "ABBOTINDIA", "PPLPHARMA",

    # FMCG / consumer
    "DABUR", "MARICO", "GODREJCP", "COLPAL", "VBL", "UBL", "RADICO",
    "PGHH", "EMAMILTD", "JUBLFOOD", "DEVYANI", "TATACONSUM", "PATANJALI",
    "BAJAJCON", "HONASA",

    # Metals / mining / energy
    "VEDL", "JINDALSTEL", "SAIL", "NMDC", "NATIONALUM", "HINDZINC",
    "ADANIENT", "ADANIGREEN", "ADANIPOWER", "ADANIENSOL", "TATAPOWER",
    "JSWENERGY", "NHPC", "SJVN", "IOC", "BPCL", "HINDPETRO", "GAIL",
    "PETRONET", "IGL", "MGL", "OIL", "GUJGASLTD",

    # Infra / capital goods / cement / realty
    "SIEMENS", "ABB", "CGPOWER", "THERMAX", "BHEL", "HAVELLS", "VOLTAS",
    "CROMPTON", "ULTRACEMCO", "SHREECEM", "AMBUJACEM", "ACC", "DALBHARAT",
    "JKCEMENT", "DLF", "GODREJPROP", "OBEROIRLTY", "PRESTIGE", "LODHA",
    "PHOENIXLTD", "IRB", "GMRINFRA", "KEC", "KALYANKJIL", "SUZLON",

    # Chemicals / others
    "PIDILITIND", "SRF", "PIIND", "AARTIIND", "DEEPAKNTR", "NAVINFLUOR",
    "TATACHEM", "UPL", "COROMANDEL", "CHAMBLFERT", "GNFC", "FACT",
    "SUPREMEIND", "ASTRAL", "APLAPOLLO", "BERGEPAINT", "KANSAINER",
    "GRASIM", "PAGEIND", "PIDILITIND", "DMART", "VBL", "MAXHEALTH",

    # Telecom / media / misc large holdings
    "IDEA", "INDUSTOWER", "TATACOMM", "SUNTV", "PVRINOX", "DELHIVERY",
    "CONCOR", "CONTAINER", "BLUEDART", "GESHIP", "SCI", "MAZDOCK",
    "COCHINSHIP", "GRSE", "BDL", "DATAPATTNS", "ZENTEC", "PARAS",
    "RVNL", "IRCON", "RAILTEL", "TEXRAIL", "TITAGARH", "JWL",

    # Popular retail / small-mid holdings
    "SWIGGY", "IREDA", "NHPC", "GREAVESCOT", "OLECTRA", "OLAELEC",
    "NELCO", "PCJEWELLER", "AREM", "SERVOTECH", "TARIL", "CCAVENUE",
    "JRMA", "RPOWER", "ADSL", "AURIONPRO", "DEEPAKNTR", "ELITECON",
    "GROWWMC150", "BBOX", "URBANCO", "PASEDIGITK", "CHAMBLFERT", "HYUNDAI",
    "HUHTAMAKI", "BLS", "EASEMYTRIP", "TATAINVEST", "AEGISLOG",
]

# De-duplicate while preserving order.
_seen = set()
UNIVERSE = [s for s in UNIVERSE if not (s in _seen or _seen.add(s))]
