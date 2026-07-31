"""
Invest.IQ — self-owned "Top 750" stock universe.

A curated, TIERED NSE universe that we control, rather than tracking a periodic
index reshuffle. Tiers are cumulative buckets by market-cap / prominence:

    Top 100  – blue-chip leaders
    Top 250  – large & upper-mid caps  (Top 100 + next 150)
    Top 500  – broad-market leaders    (Top 250 + next 250)
    Top 750  – complete AI-coverage universe (Top 500 + next 250)

Design rules (per product spec):
  • Well-known / commonly-followed companies; reasonable liquidity.
  • Long enough trading history (plus select quality recent IPOs).
  • Broad sector representation; active survivors.
  • Portfolio holdings are ALWAYS included so the owner is a live first user.

Symbols are plain NSE tickers (no ".NS"; the fetcher appends it). Over-inclusion
is safe — an unknown/renamed symbol simply fails the price fetch and is skipped,
and the daily run logs the resolve rate so the universe self-cleans over time.

`UNIVERSE` is the de-duplicated union of every tier; `TIER_OF[sym]` gives the
tightest tier a symbol belongs to (100 < 250 < 500 < 750). Keep lists sorted-ish
by prominence within a tier; duplicates across tiers are fine (deduped below).
"""

# ── Tier 1 — Top 100: blue-chip leaders ────────────────────────────────────
TIER_100 = [
    "RELIANCE", "TCS", "HDFCBANK", "ICICIBANK", "BHARTIARTL", "INFY", "SBIN",
    "LICI", "ITC", "HINDUNILVR", "LT", "BAJFINANCE", "KOTAKBANK", "HCLTECH",
    "SUNPHARMA", "MARUTI", "AXISBANK", "NTPC", "ONGC", "ADANIENT", "ADANIPORTS",
    "TITAN", "ULTRACEMCO", "ASIANPAINT", "WIPRO", "BAJAJFINSV", "POWERGRID",
    "M&M", "TATAMOTORS", "COALINDIA", "NESTLEIND", "JSWSTEEL", "TATASTEEL",
    "IOC", "HAL", "DMART", "BAJAJ-AUTO", "SIEMENS", "ADANIGREEN", "ADANIPOWER",
    "VBL", "TRENT", "PIDILITIND", "TECHM", "BEL", "GRASIM", "HINDALCO",
    "BPCL", "BRITANNIA", "GODREJCP", "EICHERMOT", "DABUR", "DIVISLAB",
    "SHREECEM", "CIPLA", "HEROMOTOCO", "APOLLOHOSP", "DRREDDY", "INDUSINDBK",
    "TATACONSUM", "BAJAJHLDNG", "SBILIFE", "HDFCLIFE", "PFC", "RECLTD",
    "IRFC", "CHOLAFIN", "TATAPOWER", "AMBUJACEM", "GAIL", "DLF", "VEDL",
    "ZOMATO", "ETERNAL", "JIOFIN", "LTIM", "PERSISTENT", "COFORGE", "MOTHERSON",
    "TVSMOTOR", "HAVELLS", "ICICIGI", "ICICIPRULI", "SBICARD", "TORNTPHARM",
    "NAUKRI", "INDIGO", "MAZDOCK", "CGPOWER", "ABB", "BOSCHLTD", "PNB",
    "BANKBARODA", "CANBK", "UNIONBANK", "IDBI", "MANKIND", "ZYDUSLIFE",
    "MAXHEALTH", "POLYCAB",
]

# ── Tier 2 — additions to reach Top 250: large & upper-mid caps ─────────────
ADD_250 = [
    "LUPIN", "AUROPHARMA", "ALKEM", "GLENMARK", "BIOCON", "IPCALAB", "LAURUSLABS",
    "ABBOTINDIA", "GLAND", "SYNGENE", "FORTIS", "PPLPHARMA", "AJANTPHARM",
    "MPHASIS", "LTTS", "OFSS", "TATAELXSI", "KPITTECH", "CYIENT", "BSOFT",
    "ZENSARTECH", "TATATECH", "SONACOMS", "UNOMINDA", "BHARATFORG", "ASHOKLEY",
    "TIINDIA", "MRF", "APOLLOTYRE", "BALKRISIND", "EXIDEIND", "SCHAEFFLER",
    "ENDURANCE", "ESCORTS", "BAJAJHFL", "SHRIRAMFIN", "MUTHOOTFIN", "BAJFINANCE",
    "LICHSGFIN", "M&MFIN", "SUNDARMFIN", "POONAWALLA", "MANAPPURAM", "IREDA",
    "FEDERALBNK", "IDFCFIRSTB", "AUBANK", "BANDHANBNK", "YESBANK", "RBLBANK",
    "INDIANB", "IOB", "UCOBANK", "CENTRALBK", "MAHABANK", "PSB",
    "PETRONET", "IGL", "MGL", "GUJGASLTD", "OIL", "HINDPETRO", "ATGL",
    "ADANIENSOL", "TATACOMM", "INDUSTOWER", "IDEA", "NHPC", "SJVN", "JSWENERGY",
    "NLCINDIA", "TATACHEM", "SRF", "PIIND", "AARTIIND", "DEEPAKNTR", "NAVINFLUOR",
    "UPL", "COROMANDEL", "CHAMBLFERT", "GNFC", "SUPREMEIND", "ASTRAL", "APLAPOLLO",
    "POLYCAB", "KEI", "FINOLEXIND", "BERGEPAINT", "KANSAINER", "PAGEIND",
    "PGHH", "COLPAL", "MARICO", "UBL", "RADICO", "EMAMILTD", "JUBLFOOD",
    "DEVYANI", "PATANJALI", "HONASA", "GODREJIND", "TATACONSUM", "BATAINDIA",
    "RELAXO", "TITAGARH", "RVNL", "IRCON", "NBCC", "KEC", "NCC", "GMRINFRA",
    "GMRAIRPORT", "IRB", "PHOENIXLTD", "GODREJPROP", "OBEROIRLTY", "PRESTIGE",
    "LODHA", "BRIGADE", "SOBHA", "JKCEMENT", "DALBHARAT", "ACC", "RAMCOCEM",
    "THERMAX", "BHEL", "VOLTAS", "CROMPTON", "WHIRLPOOL", "DIXON", "AMBER",
    "KAYNES", "SYRMA", "CDSL", "BSE", "MCX", "ANGELONE", "IEX", "CAMS",
    "KFINTECH", "360ONE", "NUVAMA", "IIFL", "SUNTV", "PVRINOX", "NAZARA",
    "DELHIVERY", "CONCOR", "BLUEDART", "GESHIP", "COCHINSHIP", "GRSE", "BDL",
    "DATAPATTNS", "SOLARINDS", "ASTERDM", "NH", "GLOBALHEALTH", "METROPOLIS",
    "LALPATHLAB", "KALYANKJIL", "TATAINVEST", "3MINDIA",
]

# ── Tier 3 — additions to reach Top 500: broad-market leaders ───────────────
ADD_500 = [
    "SAIL", "NMDC", "NATIONALUM", "HINDZINC", "JINDALSTEL", "JSL", "APLAPOLLO",
    "WELCORP", "RATNAMANI", "HINDCOPPER", "MOIL", "GRAVITA", "SANDUR",
    "TATAMETALI", "KIRLOSBROS", "KIRLOSENG", "TIMKEN", "SKFINDIA", "GRINDWELL",
    "CARBORUNIV", "CUMMINSIND", "AIAENG", "KSB", "GRAPHITE", "HEG",
    "IPCALAB", "GRANULES", "NATCOPHARM", "JBCHEPHARM", "ERIS", "CAPLIPOINT",
    "SUVENPHAR", "NEULANDLAB", "WOCKPHARMA", "SEQUENT", "SOLARA", "AARTIDRUGS",
    "GILLETTE", "PGHL", "PGHH", "HONAUT", "SCHNEIDER", "APARINDS", "VGUARD",
    "BAJAJELEC", "ORIENTELEC", "SYMPHONY", "IFBIND", "TTKPRESTIG", "STOVEKRAFT",
    "CERA", "KAJARIACER", "SOMANYCERA", "GREENPANEL", "CENTURYPLY", "GREENLAM",
    "ACE", "GREAVESCOT", "ELECON", "TRITURBINE", "PRAJIND", "HBLENGINE",
    "ISGEC", "GMMPFAUDLR", "SUPRAJIT", "GABRIEL", "JAMNAAUTO", "MINDACORP",
    "SUBROS", "SANSERA", "RKFORGE", "HAPPYFORGE", "AUTOAXLES", "LUMAXTECH",
    "FIEMIND", "PRICOLLTD", "BANCOINDIA", "TALBROAUTO", "SETCO",
    "AEGISLOG", "GUJALKALI", "GHCL", "NOCIL", "SUDARSCHEM", "VINATIORGA",
    "FINEORG", "CLEAN", "GALAXYSURF", "ROSSARI", "NEOGEN", "TATVA", "AETHER",
    "CHEMPLASTS", "EPL", "JYOTHYLAB", "DODLA", "HERITGFOOD", "HATSUN",
    "KRBL", "LTFOODS", "GODREJAGRO", "AVANTIFEED", "VENKEYS", "ZYDUSWELL",
    "TATACOFFEE", "CCL", "BIKAJI", "GOPAL", "MRSBECTORS", "PRATAAP",
    "AWL", "PATANJALI", "GODFRYPHLP", "VSTIND", "TASTYBITE",
    "SUNDRMFAST", "WABAG", "ELGIEQUIP", "KIRLOSIND", "SWARAJENG",
    "FINPIPE", "PRINCEPIPE", "TIRUMALCHM", "RATNAMANI",
    "IBULHSGFIN", "PNBHOUSING", "APTUS", "HOMEFIRST", "AAVAS", "CANFINHOME",
    "REPCOHOME", "CREDITACC", "SPANDANA", "FUSION", "UGROCAP", "FIVESTAR",
    "CSBBANK", "KARURVYSYA", "SOUTHBANK", "DCBBANK", "CITYUNIONBK", "J&KBANK",
    "EQUITASBNK", "UJJIVANSFB", "SURYODAY", "FINCABLES", "STARHEALTH",
    "NIACL", "GICRE", "MFSL", "MAXFINANCIAL",
    "RAYMOND", "ARVIND", "KPRMILL", "TRIDENT", "WELSPUNLIV", "VARDHACRLC",
    "GOKEX", "PEARLGLOBAL", "GOKALDAS", "SPAL", "RSWM", "NITINSPIN",
    "DEEPAKFERT", "MADRASFERT", "RCF", "FACT", "PARADEEP", "MANGCHEFER",
    "NFL", "ZUARIIND", "KAVERISEED", "BAYERCROP", "RALLIS", "SUMICHEM",
    "PIIND", "DHANUKA", "INSECTICID", "SHARDACROP", "BASF",
    "CAMPUS", "METROBRAND", "BATAINDIA", "KHADIM", "MIRZAINT",
    "VMART", "SHOPERSTOP", "ADITYADEL", "GOCOLORS", "TCNSBRANDS",
    "ABFRL", "RAYMONDLSL", "SENCO", "THANGAMAYL", "PCJEWELLER", "TBZ",
    "RELIGARE", "EDELWEISS", "MOTILALOFS", "PAYTM", "POLICYBZR", "NYKAA",
    "INDIAMART", "AFFLE", "ROUTE", "TANLA", "MAPMYINDIA", "LATENTVIEW",
    "INTELLECT", "NEWGEN", "RATEGAIN", "HAPPSTMNDS", "BIRLASOFT", "SONATSOFTW",
    "MASTEK", "ECLERX", "FSL", "CIGNITITEC", "KELLTONTEC", "AURIONPRO",
]

# ── Tier 4 — additions to reach Top 750: complete coverage (small/microcaps) ─
ADD_750 = [
    "SUZLON", "INOXWIND", "ORIENTGREEN", "KPIGREEN", "WAAREE", "PREMIERENE",
    "GENSOL", "ADANIENSOL", "NTPCGREEN", "ACMESOLAR", "SWSOLAR", "BOROSCI",
    "TARIL", "SHILCHAR", "VOLTAMP", "TRANSWIND", "DANISH", "URJA",
    "HBLENGINE", "POWERINDIA", "GEVERNOVA", "TDPOWERSYS", "CGPOWER", "APAR",
    "RTNPOWER", "RPOWER", "JPPOWER", "JSWENERGY", "TATAPOWER", "NHPC", "SJVN",
    "IREDA", "PTC", "IEX", "INDIGOPNTS", "AKZOINDIA", "SIRCA",
    "OLECTRA", "OLAELEC", "JBMA", "FIEMIND", "GREAVESCOT", "SMLISUZU",
    "VSTTILLERS", "SWARAJENG", "ESCORTS", "ACE", "BEML", "TITAGARH", "JWL",
    "TEXRAIL", "RAILTEL", "IRCTC", "RITES", "RVNL", "IRCON", "CONCOR",
    "IRFC", "RAILVIKAS", "KERNEX", "SALASAR",
    "NELCO", "TEJASNET", "HFCL", "STLTECH", "ITI", "GTLINFRA", "RAILTEL",
    "ZENTEC", "DATAPATTNS", "PARAS", "MTARTECH", "AZAD", "UNIMECH", "IDEAFORGE",
    "DCXINDIA", "BBOX", "SANSERA", "CYIENTDLM", "KAYNES", "SYRMA", "AVALON",
    "SERVOTECH", "EXICOM", "ELIN", "PGEL", "EPACK", "AMBER", "DIXON",
    "ADSL", "AURIONPRO", "INTELLECT", "NEWGEN", "SUBEXLTD", "BLS", "EMUDHRA",
    "CCAVENUE", "INFIBEAM", "IKIO", "ZAGGLE", "MOSCHIP", "SPICEJET",
    "SWIGGY", "PBFINTECH", "PAYTM", "EASEMYTRIP", "IXIGO", "RATEGAIN",
    "NAZARA", "DELTACORP", "ONMOBILE", "SAREGAMA", "TIPSMUSIC", "PVRINOX",
    "NETWORK18", "TV18BRDCST", "ZEEL", "DISHTV", "HATHWAY", "DEN",
    "URBANCO", "HYUNDAI", "TATACAP", "TMPV", "PASEDIGITK", "AREM",
    "GROWWMC150", "ELITECON", "JRMA", "HUHTAMAKI", "GRWRHITECH", "PIXTRANS",
    "SHAKTIPUMP", "KIRLPNU", "ROTO", "WPIL", "JASH", "ATLASCYCLE",
    "PPLPHARMA", "WINDLAS", "GLENMARK", "MEDPLUS", "APOLLO", "RAINBOW",
    "KIMS", "YATHARTH", "SHALBY", "KRSNAA", "VIJAYA", "THYROCARE", "DRLALPATH",
    "POKARNA", "PGIL", "SPCENET", "PARKHOTELS", "CHALET", "LEMONTREE",
    "EIHOTEL", "INDHOTEL", "MHRIL", "TAJGVK", "ORIENTHOT", "ROHLTD",
    "IRB", "ASHOKA", "PNCINFRA", "KNRCON", "HGINFRA", "GRINFRA", "JKIL",
    "CAPACITE", "AHLUCONT", "ITDCEM", "PSPPROJECT", "RITES", "ENGINERSIN",
    "GPTINFRA", "MODISON", "TARC", "KOLTEPATIL", "MAHLIFE", "ARVSMART",
    "SUNTECK", "ANANTRAJ", "SIGNATURE", "MAHINDCIE", "SHRIRAMPPS",
    "GRSE", "COCHINSHIP", "MAZDOCK", "BDL", "BEL", "HAL", "MIDHANI", "BEML",
    "APCOTEXIND", "NOCIL", "BALAMINES", "ALKYLAMINE", "JUBLINGREA", "PCBL",
    "HIMATSEIDE", "FILATEX", "GARFIBRES", "SPLPETRO", "NAHARSPING",
    "AGARIND", "SHREEPUSHK", "TATVA", "DHARANI",
]

# ── Portfolio holdings — ALWAYS included (owner is the live first user) ──────
PORTFOLIO = [
    "TMPV", "PASEDIGITK", "CHAMBLFERT", "ETERNAL", "SERVOTECH", "COCHINSHIP",
    "SUZLON", "TRENT", "AREM", "M&M", "SWIGGY", "IREDA", "TATAPOWER", "GAIL",
    "NELCO", "ICICIBANK", "PCJEWELLER", "GREAVESCOT", "ELITECON", "CROMPTON",
    "RPOWER", "ADSL", "CCAVENUE", "JRMA", "SBICARD", "NHPC", "POONAWALLA",
    "HDFCBANK", "ZENTEC", "EXIDEIND", "TEXRAIL", "EASEMYTRIP", "CYIENTDLM",
    "TATAELXSI", "HUHTAMAKI", "BLS", "HYUNDAI", "BSE", "JSWENERGY", "TATAINVEST",
    "RELIANCE", "AURIONPRO", "DEEPAKNTR", "BAJFINANCE", "SIEMENS", "OLAELEC",
    "TATACAP", "KPITTECH", "URBANCO", "TARIL", "BBOX", "GROWWMC150", "RECLTD",
    "LT", "ADANIPORTS",
]


def _dedupe(seq):
    seen = set()
    out = []
    for s in seq:
        s = s.strip().upper()
        if s and s not in seen:
            seen.add(s)
            out.append(s)
    return out


# Tightest tier each symbol belongs to (lower number = higher tier).
TIER_OF = {}
for _sym in _dedupe(TIER_100):
    TIER_OF.setdefault(_sym, 100)
for _sym in _dedupe(ADD_250):
    TIER_OF.setdefault(_sym, 250)
for _sym in _dedupe(ADD_500):
    TIER_OF.setdefault(_sym, 500)
for _sym in _dedupe(ADD_750):
    TIER_OF.setdefault(_sym, 750)
# Portfolio names not already tiered are treated as the broad (750) coverage.
for _sym in _dedupe(PORTFOLIO):
    TIER_OF.setdefault(_sym, 750)

# Full de-duplicated universe (order: prominence tiers first, then portfolio).
UNIVERSE = _dedupe(
    _dedupe(TIER_100) + _dedupe(ADD_250) + _dedupe(ADD_500)
    + _dedupe(ADD_750) + _dedupe(PORTFOLIO)
)

# Convenience cumulative tier sets.
TOP_100 = [s for s in UNIVERSE if TIER_OF.get(s, 999) <= 100]
TOP_250 = [s for s in UNIVERSE if TIER_OF.get(s, 999) <= 250]
TOP_500 = [s for s in UNIVERSE if TIER_OF.get(s, 999) <= 500]
TOP_750 = list(UNIVERSE)
