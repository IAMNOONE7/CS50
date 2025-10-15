import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from yahooquery import Ticker
from datetime import date
import pandas as pd
from flask import jsonify, request
import numpy as np
import time

from helpers import apology, login_required, usd, fetch_live_prices, compute_closed_trades, range_to_params, _build_payload
#=================================
_HIST_CACHE = {}
_HIST_TTL_S = 60

_QUOTE_CACHE = {}
_QUOTE_TTL_S = 10

_QUOTES_CACHE = {}
_QUOTES_TTL_S = 10
#=================================

app = Flask(__name__)
app.jinja_env.filters["usd"] = usd
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
db = SQL("sqlite:///stocks.db")

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide username")
        if not password:
            return apology("must provide password")
        if password != confirmation:
            return apology("passwords must match")

        try:
            new_id = db.execute(
                "INSERT into users (username, hash) VALUES (?,?)", username, generate_password_hash(password),
            )
        except Exception:
            return apology("username already exists")

        session["user_id"] = new_id
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username:
            return apology("must provide username", 403)

        if not password:
            return apology("must provide password", 403)

        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)

        session["user_id"] = rows[0]["id"]
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/trade", methods=["GET", "POST"])
@login_required
def trade():
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = (request.form.get("symbol") or "").upper().strip()
        side = request.form.get("side")
        shares = request.form.get("shares")
        use_live = request.form.get("use_live") == "1"
        price_in = request.form.get("price")

        if not symbol:
            return apology("missing symbol")
        try:
            shares = int(shares)
        except (TypeError, ValueError):
            return apology("shares must be a positive integer")
        if shares <= 0:
            return apology("shares must be a positive integer")

        if use_live:
            price = fetch_live_prices([symbol]).get(symbol)
            if price is None:
                return apology("could not fetch live price")

        else:
            try:
                price = float(price_in)
            except (TypeError, ValueError):
                return apology("invalid price")
            if price <= 0:
                return apology("invalid price")

        fees = 0.0

        rows = db.execute(
            "SELECT shares, avg_cost FROM positions WHERE user_id = ? AND symbol = ?", user_id, symbol,
        )

        pos = rows[0] if rows else None

        if side == "buy":
            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price, fees) VALUES (?,?,?,?,?)", user_id, symbol, shares, price, fees
            )

            if pos:
                old_sh, old_avg = pos["shares"], float(pos["avg_cost"])
                new_sh = old_sh + shares
                new_cost_total = old_sh * old_avg + shares * price + fees
                new_avg = new_cost_total/new_sh
                db.execute(
                    "UPDATE positions SET shares = ?, avg_cost = ? WHERE user_id = ? AND symbol = ?", new_sh, new_avg, user_id, symbol
                )
            else:
                db.execute(
                    "INSERT INTO positions (user_id, symbol, shares, avg_cost) VALUES (?,?,?,?)", user_id, symbol, shares, price
                )
        elif side == "sell":
            if not pos or pos["shares"] < shares:
                return apology("too many shares")

            db.execute(
                "INSERT INTO transactions (user_id, symbol, shares, price, fees) VALUES (?, ?, ?, ?, ?)",user_id, symbol, -shares, price, fees
            )

            new_sh = pos["shares"] - shares
            if new_sh ==0:
                db.execute(
                    "DELETE FROM positions WHERE user_id = ? AND symbol = ?", user_id, symbol
                )

            else:
                db.execute(
                    "UPDATE positions SET shares = ? WHERE user_id = ? AND symbol = ?",
                    new_sh, user_id, symbol
                )

        else:
            return apology("invalid state")

        return redirect("/positions")

    return render_template("trade.html")

@app.route("/positions")
@login_required
def positions():
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, shares, avg_cost FROM positions WHERE user_id = ? ORDER BY symbol",
        user_id,
    )
    symbols = [r["symbol"] for r in rows]
    quotes = fetch_live_prices(symbols)

    for r in rows:
        last = quotes.get(r["symbol"])
        r["last"] = last
        if last is None:
            r["unrealized"] = None
            r["unrealized_pct"] = None
        else:
            r["unrealized"] = (last - float(r["avg_cost"])) * r["shares"]
            r["unrealized_pct"] = (last / float(r["avg_cost"]) - 1.0) *100.0

    total_value = sum((r["last"] * r["shares"]) for s in rows if r["last"] is not None)
    return render_template("positions.html", rows = rows, total_value = total_value)


@app.route("/closed")
@login_required
def closed():
    user_id = session["user_id"]
    rows = compute_closed_trades(user_id, db)
    total_realized = sum(r["pnl"] for r in rows)
    return render_template("closed.html", rows=rows, total_realized = total_realized)


@app.route("/symbol/<symbol>")
@login_required
def symbol(symbol):
    user_id = session["user_id"]
    symbol = symbol.upper().strip()

    trades = db.execute(
        "SELECT shares, price, executed_at FROM transactions WHERE user_id = ? AND symbol = ? ORDER BY executed_at ASC", user_id, symbol
    )
    markers = []
    for t in trades:
        is_buy = t["shares"] > 0
        markers.append({
            "time": str(t["executed_at"])[:10],
            "position": "belowBar" if is_buy else "aboveBar",
            "color": "#2ecc71" if is_buy else "#e74c3c",
            "shape": "arrowUp" if is_buy else "arrowDown",
            "text": f"{'Buy' if is_buy else 'Sell'} {abs(t['shares'])} @ ${t['price']:,.2f}"
        })

    return render_template("symbol.html", symbol=symbol, markers=markers, trades=trades)


@app.route("/api/quote")
@login_required
def api_quote():
    symbol = (request.args.get("symbol") or "").upper().strip()
    if not symbol:
        return jsonify(ok=False)
    now = time.time()
    if symbol in _QUOTE_CACHE and now - _QUOTE_CACHE[symbol][0] < _QUOTE_TTL_S:
            return jsonify(ok=True, **_QUOTE_CACHE[symbol][1])

    try:
        t = Ticker(symbol)
        price = t.price or {}
        node = price.get(symbol) or price.get(symbol.upper()) or price.get(symbol.lower()) or {}
        last = node.get("regularMarketPrice")
        prev = node.get("regularMarketPreviousClose")
        chg = (last - prev) if (last is not None and prev is not None) else None
        pct = (chg / prev *100.0) if (chg is not None and prev not in (None,0)) else None
        payload = {
            "symbol": symbol,
            "last": last,
            "previousClose": prev,
            "change": chg,
            "changePercent": pct,
            "currency": node.get("currency")
        }

        _QUOTE_CACHE[symbol] = (now, payload)
        return jsonify(ok = True, **payload)
    except Exception:
        return jsonify(ok=False)




@app.route("/api/history")
@login_required
def api_history():
    symbol  = (request.args.get("symbol") or "").upper().strip()
    range_  = request.args.get("range")
    period  = request.args.get("period")
    interval= request.args.get("interval")
    if not symbol:
        return jsonify(data=[])

    if range_:
        params = range_to_params(range_)
    else:
        params = {"period": (period or "2y"), "interval": (interval or "1d"), "fallbacks": ["1wk"]}

    cache_key = (symbol, params.get("period"), params.get("interval"),
                 params.get("start"), params.get("end"))
    now = time.time()
    if cache_key in _HIST_CACHE and now - _HIST_CACHE[cache_key][0] < _HIST_TTL_S:
        return jsonify(data=_HIST_CACHE[cache_key][1])

    try:
        t = Ticker(symbol)
        intervals_to_try = [params["interval"]] + params.get("fallbacks", [])
        for iv in intervals_to_try:
            if params.get("start"):
                df = t.history(start=params["start"], end=params.get("end"),
                               interval=iv, adj_ohlc=True)
            else:
                df = t.history(period=params.get("period","2y"),
                               interval=iv, adj_ohlc=True)

            try:
                if len(df) == 0:
                    continue
            except Exception:
                continue

            payload = _build_payload(df, symbol, iv)
            if payload:
                _HIST_CACHE[cache_key] = (now, payload)
                return jsonify(data=payload)

        return jsonify(data=[])
    except Exception:
        return jsonify(data=[])


@app.route("/api/quotes")
@login_required
def api_quotes():
    raw = (request.args.get("symbols") or "").strip()
    symbols = sorted({s.upper() for s in raw.split(",") if s.strip()})
    if not symbols:
        return jsonify(data=[]),400

    key = tuple(symbols)
    now = time.time()
    if key in _QUOTES_CACHE and now - _QUOTES_CACHE[key][0] < _QUOTES_TTL_S:
        return jsonify(data=_QUOTES_CACHE[key][1])

    try:
        t=Ticker(symbols, asynchronous = True)
        price = t.price or {}

        out = []
        for s in symbols:
            node = price.get(s) or price.get(s.upper()) or price.get(s.lower()) or {}
            last = node.get("regularMarketPrice")
            prev = node.get("regularMarketPreviousClose")
            chg  = (last - prev) if (last is not None and prev is not None) else None
            pct  = (chg / prev * 100.0) if (chg is not None and prev not in (None, 0)) else None
            out.append({
                "symbol": s,
                "name": node.get("shortName") or node.get("longName") or s,
                "last": last,
                "prev": prev,
                "chg": chg,
                "pct": pct,
                "currency": node.get("currency"),
            })

        _QUOTES_CACHE[key] = (now,out)
        return jsonify(data=out)
    except Exception as e:
        return jsonify(data=[], error=str(e)),500


@app.route("/watchlist", methods=["GET","POST"])
@login_required
def watchlist():
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = (request.form.get("symbol") or "").upper().strip()
        if symbol:
            if request.form.get("remove"):
                db.execute("DELETE FROM watchlist WHERE user_id=? AND symbol=?",user_id, symbol)
            else:
                db.execute("INSERT OR IGNORE INTO watchlist (user_id, symbol) VALUES(?,?)",user_id, symbol)
        return redirect("/watchlist")

    rows=db.execute("SELECT symbol FROM watchlist WHERE user_id=? ORDER BY symbol", user_id)
    symbols = [r["symbol"] for r in rows]
    return render_template("watchlist.html", symbols=symbols)
