import requests
from flask import redirect, render_template, session
from functools import wraps
from yahooquery import Ticker
from datetime import datetime
from collections import deque
import numpy as np
import pandas as pd
from datetime import date, timedelta
from markupsafe import escape

def apology(message, code=400):
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def usd(value):
    return f"${value:,.2f}"

def fetch_live_prices(symbols):
    if not symbols:
        return {}

    t = Ticker(" ".join(symbols))
    out = {}
    data = t.price
    for s in symbols:
        try:
            out[s] = data[s]["regularMarketPrice"]
        except Exception:
            out[s] = None
    return out


def compute_closed_trades(user_id, db):
    tx = db.execute(
        "SELECT symbol, shares, price, executed_at FROM transactions WHERE user_id = ? ORDER BY executed_at ASC, id ASC", user_id,
    )

    closed = []
    queues = {}

    for r in tx:
        sym = r["symbol"]
        sh = int(r["shares"])
        px = float(r["price"])
        dt = datetime.fromisoformat(str(r["executed_at"]))

        if sh>0:
            queues.setdefault(sym, deque()).append({"qty": sh, "price": px, "dt": dt})
        elif sh<0:
            qty = -sh
            q = queues.setdefault(sym,deque())
            while qty > 0 and q:
                lot = q[0]
                take = min(qty, lot["qty"])
                pnl = (px - lot["price"]) * take
                ret = (px / lot["price"] - 1.0) * 100.0
                days = (dt - lot["dt"]).days
                closed.append({
                    "symbol": sym,
                    "qty": take,
                    "entry_price": lot["price"],
                    "exit_price": px,
                    "opened_at": lot["dt"].date().isoformat(),
                    "closed_at": dt.date().isoformat(),
                    "pnl": pnl,
                    "pnl_pct": ret,
                    "days": days,
                })
                lot["qty"] -= take
                qty -= take
                if lot["qty"] == 0:
                    q.popleft()
    return closed

def fetch_prices_and_history_ohlc(tickers, period="2y", interval="1d", adjusted=True):
    tickers = [str(t).upper() for t in tickers]
    t = Ticker(tickers, asynchronous=True)
    price_raw = t.price or {}
    px = pd.DataFrame(price_raw).T.reset_index().rename(columns={"index":"ticker"})
    want = ["preMarketPrice","regularMarketOpen","regularMarketPreviousClose","regularMarketPrice"]
    for c in want:
        if c not in px.columns:
            px[c] = np.nan
    prices_df = (
        px.set_index("ticker")[want]
          .rename(columns={
              "preMarketPrice":"pre",
              "regularMarketOpen":"open",
              "regularMarketPreviousClose":"prev_close",
              "regularMarketPrice":"last"
          })
    )
    for c in prices_df.columns:
        prices_df[c] = pd.to_numeric(prices_df[c], errors="coerce")
    hist = t.history(period=period, interval=interval, adj_ohlc=adjusted)
    if not isinstance(hist, pd.DataFrame) or hist.empty:
        return prices_df, pd.DataFrame()

    df = hist.reset_index()
    if "symbol" in df.columns:
        df = df.rename(columns={"symbol":"ticker"})
    if "ticker" not in df.columns and len(tickers) == 1:
        df["ticker"] = tickers[0]
    if "adjclose" in df.columns:
        df["close"] = df["adjclose"]
    for c in ["open","high","low","close","volume"]:
        if c not in df.columns:
            df[c] = np.nan

    df["date"] = pd.to_datetime(df["date"]).dt.tz_localize(None).dt.date.astype(str)
    for c in ["open","high","low","close","volume"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    hist_df = (
        df[["ticker","date","open","high","low","close","volume"]]
        .set_index(["ticker","date"])
        .sort_index()
    )
    return prices_df, hist_df

def _safe_date(year, month, day):
    try:
        return date(year, month, day)
    except:
        return date(year, month, 28)


def range_to_params(r: str):
    r = (r or "").lower()
    today = date.today()

    if r == "1d":
        return {"period": "1d", "interval": "2m", "fallbacks": ["5m", "15m", "30m"]}
    if r == "5d":
        return {"period": "5d", "interval": "15m", "fallbacks": ["30m", "60m"]}
    if r in ("week", "1w"):
        return {"period": "7d", "interval": "60m", "fallbacks": ["90m", "1h", "1d"]}
    if r in ("month", "1m"):
        return {"period": "1mo", "interval": "60m", "fallbacks": ["1d"]}
    if r in ("3m", "3month", "3months"):
        return {"period": "3mo", "interval": "1d", "fallbacks": ["1wk"]}
    if r == "ytd":
        start = _safe_date(today.year, 1, 1).isoformat()
        end = today.isoformat()
        return {"start": start, "end": end, "interval": "1d", "fallbacks": ["1wk"]}
    if r == "5y":
        five = _safe_date(today.year - 5, today.month, today.day).isoformat()
        return {"start": five, "end": today.isoformat(), "interval": "1wk", "fallbacks": ["1mo"]}
    # default
    return {"period": "2y", "interval": "1d", "fallbacks": ["1wk"]}


def _is_intraday(interval:str):
    return any(interval.endswith(suf) for suf in ("m","h"))


def _build_payload(df: pd.DataFrame, symbol:str, interval:str):
    df = df.reset_index()
    if "symbol" in df.columns:
        df = df[df["symbol"].astype(str).str.upper() == symbol]

    if "adjclose" in df.columns:
        df["close"] = df["adjclose"]

    need = {"open", "high", "low", "close", "date"}
    if not need.issubset(df.columns):
        return []

    ts = pd.to_datetime(df["date"], utc=True, errors="coerce")
    df = df.assign(open=pd.to_numeric(df["open"], errors="coerce"),
                   high=pd.to_numeric(df["high"], errors="coerce"),
                   low =pd.to_numeric(df["low"],  errors="coerce"),
                   close=pd.to_numeric(df["close"],errors="coerce"))
    df = df.dropna(subset=["open","high","low","close","date"]).copy()

    intraday = _is_intraday(interval)
    if intraday:
        # Unix seconds for intraday
        df["time"] = (ts.view("int64") // 1_000_000_000).astype("int64")
    else:
        df["time"] = ts.dt.strftime("%Y-%m-%d")

    df = df.sort_values("time")

    return [
        {"time": t, "open": float(o), "high": float(h), "low": float(l), "close": float(c)}
        for t, o, h, l, c in df[["time","open","high","low","close"]].itertuples(index=False, name=None)
    ]
