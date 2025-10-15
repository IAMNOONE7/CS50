# TRADES WATCHER
#### Description: A lightweight stock-tracking web app that let's users refister/login, recod buy/sell trades, monitor open and closed positions with live quotes, keep a watchlist, and explore interactive charts (1D, 5D, Week, 3M, YTD, 5Y).

---

## Overview
This project is a personal trading journal and portfolio tracker built on Flask + SQLite. It focuses on speed of use (single-screen trade entry), clarity (open vs. closed positions), and quick exploration (interactive charts and a watchlist). Prices and historical data come from **yahooquery**; charts are rendered with **Lightweight charts** in the browser.

Primary goals:
1. Log trades quickly (buy/sell entries), then calculate P&L automatically.
2. See all **open** positions with live prices and unrealized P&L.
3. Review **closed** positions with profit in $ and %.
4. Maintain a **watchlist** of tickers with live quotes and quick links to charts.

---

## Features
- **Auth**: register, login, logout; registration enforces **password confirmation**.
- **Positions**: table of all open holdings, live last price, position value, cost basis, and unrealized P&L.
- **Closed**: history of completed trades with realized P&L (amount and percent) and dates.
- **Watchlist**: add/remove tickers, see last/Δ/Δ% refreshed every 15s, click through to charts.
- **Trade**: add new **buy** or **sell** entries; the app updates allocations and P&L automatically.
- **Symbol page & Charts**:
    - Interactive candlesticks with pan/zoom, markers, for your trades.
    - Range switcher: **1D, 5D, Week, 3M, YTD, 5Y** (with sensible intraday/daily intervals).
    - "Go to symbol" box in the navbar for fast navigation.
- **Caching**: light server-side caching of quotes/history to reduce API calls and improve responsivnes.
- **Responsive UI**: Bootstrap 4

---

## How to use
1. Register an account, then log in.
2. Open the Trade tab to create a buy entry: choose symbol, shares, and price, then submit.
3. Your new positions appears in Positions with live updates to value and unrealized P&L.
4. Record a sell entry in Trade; once a position is fully closed, it moves to Closed with realized P&L.
5. Add tickers to watchlist to monitor last price and daily change; click a ticker to open its chart.
6. On a symbol page you can scrool, zoom, and switch ranges. Trades you recorded appear as markers.


## Architecture
- Backend: Flask (Python), templated HTML, SQLite via cs50's SQL.
- Frontend: Bootstrap 4; client-side JS for quotes refresh and charts.
- Data:
    - yahooquery for quotes and history
    - Optional static/companies.json provides ticker autocomplete

## Key routes/APIs
- GET / -> Positions
- GET /closed -> Closed positions
- Get /watchlsit (+ POST add/remove)
- GET /trade (+ POST buy/sell)
- GET /symbol/<SYM> -> symbol page with chart
- GET /login, POST /login, GET /register, POST /register, GET /logout

## Files in this project
- app.py - Flask app
- helpers.py - help codes
- templates/layout.html - site shell - navbar with quick symbol jump
- static/styles.css - small custom styles
- static/companies.json - optional autocomplete source
- stocks.db - SQLite database
- README.md - this codument

## Limitations & Future Work
- No multi-currency handling yet. currency is shown but P&L is assumed in the quote currency
- No advanced order types or partial close attribution - currently simple share math
- Planned enhancements:
    - Per-symbol analytics
    - Import from CSV
    - Tagging strategies and filtering
    - ....


