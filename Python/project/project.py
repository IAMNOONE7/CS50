import json
import pandas as pd
from pathlib import Path
import numpy as np
from yahooquery import Ticker

class Company:
    ticker:str
    cik:str = None
    sector:str = None
    industry:str = None
    is_big_index:bool = None


def load_companies(json_path):
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        rows = data.get("companies",[])
        df = pd.DataFrame(rows)
        df["ticker"] = df["ticker"].str.upper().str.strip()
        return df
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {json_path}")
    except Exception as e:
        raise RuntimeError(f"Unexpected error while loading {json_path}: {e}")

def fetch_prices_and_history(tickers, _period="1y", history_interval="1d"):
    t = Ticker(list(tickers), asynchronous=True)

    price_raw = t.price
    prices_df = pd.DataFrame(price_raw).T.reset_index().rename(columns = {"index":"ticker"})
    wanted = ["preMarketPrice", "regularMarketOpen",
              "regularMarketPreviousClose", "regularMarketPrice"]

    for c in wanted:
        if c not in prices_df.columns:
            prices_df[c] = np.nan

    prices_df = prices_df.set_index("ticker")[wanted]

    for c in wanted:
        prices_df[c] = pd.to_numeric(prices_df[c], errors="coerce")

    num_cols = ["preMarketPrice", "regularMarketOpen", "regularMarketPreviousClose","regularMarketPrice"]

    for c in num_cols:
        if c in prices_df.columns:
            prices_df[c] = pd.to_numeric(prices_df[c], errors = "coerce")

    hist = t.history(period=_period, interval=history_interval, adj_ohlc=True)

    if isinstance(hist.index, pd.MultiIndex):
        hist_df = hist.rename_axis(index={"symbol": "ticker"}).reset_index().set_index(["ticker", "date"])
    else:
        # rare single-ticker shape
        hist_df = hist.copy()
        hist_df["ticker"] = list(tickers)[0]
        hist_df = hist_df.reset_index().set_index(["ticker", "date"])

    if "adjclose" in hist_df.columns:
        hist_df = hist_df.rename(columns={"adjclose": "close"})
    if "close" not in hist_df.columns and "close" in hist.columns:
        hist_df["close"] = hist["close"]

    hist_df["close"] = pd.to_numeric(hist_df["close"], errors="coerce")
    hist_df = hist_df[["close"]]

    return prices_df, hist_df

def last_year_median_from_history(hist_df):
    s = pd.to_numeric(hist_df["close"], errors="coerce")
    s = s[s>0]
    return s.groupby(level="ticker").median()

def sma_from_history(hist_df, window = 50):
    s = pd.to_numeric(hist_df["close"], errors="coerce")
    s = s[s>0]
    return s.groupby(level="ticker").apply(lambda s: s.tail(window).mean())

def pct_change(a,b):
    a_s = pd.to_numeric(pd.Series(a), errors = "coerce")
    b_s = pd.to_numeric(pd.Series(b), errors = "coerce")
    return (a_s - b_s) / b_s.replace(0, np.nan)

def build_dashboard(companies_df, prices_df, hist_df, sma_window=50):
    base = companies_df.set_index("ticker").copy()

    #live prices
    base["before_open_price"] = prices_df["preMarketPrice"]
    base["last_open_price"] = prices_df["regularMarketOpen"]
    base["last_close_price"] = prices_df["regularMarketPreviousClose"]
    base["before_open_price"] = base["before_open_price"].fillna(prices_df["regularMarketPrice"])

    #night move
    base["pct_chg_night_vs_close"] = pct_change(base["before_open_price"], base["last_close_price"])

    #last-year median vs last close
    median_1y = last_year_median_from_history(hist_df).rename("median_1y")
    base = base.join(median_1y)
    base["pct_chg_close_vs_median1y"] = pct_change(base["last_close_price"], base["median_1y"])

    #SMA vs last close
    sma = sma_from_history(hist_df, window = sma_window).rename(f"sma{sma_window}")
    base = base.join(sma)
    base[f"pct_chg_close_vs_sma{sma_window}"] = pct_change(base["last_close_price"], base[f"sma{sma_window}"])

    #rank
    m1 = "pct_chg_close_vs_median1y"
    m2 = f"pct_chg_close_vs_sma{sma_window}"

    rankable = base[[m1,m2]].dropna().copy()

    r1 = rankable[m1].rank(ascending = True, method = "min")
    r2 = rankable[m2].rank(ascending = True, method = "min")

    total_score = r1 + r2
    total_rank = total_score.rank(ascending=True, method="dense")

    rank_table = pd.DataFrame({
        "rank_median1y":r1,
        f"rank_sma{sma_window}":r2,
        "total_score": total_score,
        "total_rank": total_rank
    })
    base = base.join(rank_table)
    base = base.loc[~base["total_rank"].isna()].copy()

    out = base.reset_index().rename(columns = {"ticker":"Ticker"})

    price_cols = ["before_open_price", "last_close_price","median_1y", f"sma{sma_window}"]
    pct_cols = ["pct_chg_night_vs_close","pct_chg_close_vs_median1y",f"pct_chg_close_vs_sma{sma_window}"]

    for c in price_cols:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors = "coerce").round(2)

    for c in pct_cols:
        if c in out.columns:
            out[c] = (pd.to_numeric(out[c], errors = "coerce") *100).round(2)

    for c in ["rank_median1y",  f"rank_sma{sma_window}",  "total_rank"]:
        if c in out.columns:
            out[c] = out[c].astype("Int64")

    cols = [
        "Ticker",
        "before_open_price",
        "last_close_price",
        "pct_chg_night_vs_close",
        "median_1y",
        "pct_chg_close_vs_median1y",
        f"sma{sma_window}",
        f"pct_chg_close_vs_sma{sma_window}",
        "rank_median1y",
        f"rank_sma{sma_window}",
        "total_rank",
        "sector", "industry", "is_big_index",
    ]
    cols = [c for c in cols if c in out.columns]
    return out[cols].sort_values(["total_rank"], kind="mergesort")

def export_to_excel(df, path):
    path=Path(path)
    with pd.ExcelWriter(path, engine = "openpyxl") as xl:
        df.to_excel(xl, sheet_name = "Daily Stock News", index = False)


def main(companies_json = "companies.json", output_xlsx = "daily_stock_news.xlsx", sma_window = 50):
    base_dir = Path(__file__).resolve().parent
    companies_path = base_dir/companies_json
    output_path = base_dir/output_xlsx
    companies = load_companies(companies_path)
    print(f"companies loaded: {len(companies)}")
    try:
        tickers = companies["ticker"].dropna().unique().tolist()
        print("Fetching history and prices")
        prices_df, hist_df = fetch_prices_and_history(tickers)
        print("History and prices fetched")
        print("Building dashboard")
        dashboard = build_dashboard(companies, prices_df, hist_df, sma_window = sma_window)
        print("Exporting to excel")
        export_to_excel(dashboard, output_path)
        print(f"Saved: {output_path} (rows: {len(dashboard)})")
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
