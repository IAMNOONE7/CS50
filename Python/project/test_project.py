import json
from pathlib import Path
import numpy as np
import pandas as pd


from project import load_companies, last_year_median_from_history, sma_from_history, pct_change, build_dashboard, export_to_excel



# Helpers - No live data
def _companies_df():
    return pd.DataFrame(
        [
            {"ticker":"AAA","sector":"Tech"},
            {"ticker":"BBB","sector":"Health"},
            {"ticker":"CCC","sector":"Finance"},
        ]
    )

def _prices_df():
    return pd.DataFrame(
        {
            "preMarketPrice":[10.5,20.0,np.nan],
            "regularMarketOpen":[10.0,20.0,30.0],
            "regularMarketPreviousClose":[10.0,20.0,30.0],
            "regularMarketPrice":[10.0,19.8,29.5],
        },
        index=["AAA","BBB","CCC"],
    )

def _hist_df():
    idx = pd.MultiIndex.from_product(
        [["AAA","BBB","CCC"], pd.date_range("2025-01-01", periods=6, freq="D")],
        names=["ticker","date"],
    )
    closes = (
        [10,11,12,13,14,15]+
        [20,21,22,23,24,25]+
        [30,31,32,33,34,35]
    )
    return pd.DataFrame({"close":closes}, index=idx)


#Tests

def test_load_companies(tmp_path:Path):
    data = {
        "schema_version":"1.0",
        "companies":[
            {
                "ticker":"aaa"
            },
            {
                "ticker":"bbb"
            },
        ],
    }
    p = tmp_path / "companies.json"
    p.write_text(json.dumps(data), encoding="utf-8")
    df = load_companies(p)
    assert df.shape[0] == 2
    assert df.loc[0,"ticker"] == "AAA"
    assert df.loc[1,"ticker"] == "BBB"

def test_last_year_median_from_history():
    hist = _hist_df()
    med = last_year_median_from_history(hist)
    assert np.isclose(med.loc["AAA"],12.5)
    assert np.isclose(med.loc["BBB"],22.5)
    assert np.isclose(med.loc["CCC"],32.5)

def test_sma_from_history():
    hist = _hist_df()
    sma = sma_from_history(hist,window = 3)
    assert np.isclose(sma.loc["AAA"], (13+14+15)/3)
    assert np.isclose(sma.loc["BBB"], (23+24+25)/3)

def test_pct_change():
    out = pct_change(pd.Series([110,np.nan]), pd.Series([100,50]))
    assert np.isclose(out.iloc[0],0.10)
    assert np.isnan(out.iloc[1])

def test_build_dashboard(tmp_path:Path):
    companies = _companies_df()
    prices = _prices_df()
    hist = _hist_df()

    out = build_dashboard(companies, prices, hist, sma_window = 3)

    cols={
        "Ticker", "before_open_price", "last_close_price",
        "pct_chg_night_vs_close", "median_1y", "pct_chg_close_vs_median1y",
        "sma3", "pct_chg_close_vs_sma3",
        "rank_median1y", "rank_sma3", "total_rank"
    }

    assert cols.issubset(out.columns)

    assert(out["before_open_price"].apply(lambda x:float(x).as_integer_ratio()[1]) <= 50).all()
    assert(out["pct_chg_close_vs_median1y"].abs() <= 1000).all()
    assert out["rank_median1y"].notna().all()
    assert out["rank_sma3"].notna().all()
    assert out["total_rank"].notna().all()
    assert out["total_rank"].min() == 1


def test_export_to_excel(tmp_path:Path):
    df = pd.DataFrame(
        {"Ticker": ["AAA"], "before_open_price":[10.0], "total_rank":[1]}
    )
    xlsx = tmp_path / "report.xlsx"
    export_to_excel(df,xlsx)
    assert xlsx.exists() and xlsx.stat().st_size>0

