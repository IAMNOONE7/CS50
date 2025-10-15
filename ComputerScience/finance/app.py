import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    user_id = session["user_id"]
    if not user_id:
        session.clear()
        return redirect("/login")

    row = db.execute("SELECT cash FROM users WHERE id= ?", user_id)[0]
    cash = row["cash"]

    positions = db.execute("SELECT symbol, shares FROM holdings WHERE user_id = ? AND shares >0 ORDER BY symbol", user_id,)

    total = cash
    for p in positions:
        quote = lookup(p["symbol"])
        price = quote["price"] if quote else 0
        p["price"] = price
        p["name"] = quote["name"] if quote else p["symbol"]
        p["value"] = price * p["shares"]
        total += p["value"]
    return render_template("index.html", positions = positions, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol")
        try:
            shares = int(shares)
        except(TypeError, ValueError):
            return apology("shares must be a positive integer")
        if shares <=0:
            return apology("shares must be a positive integer")

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol")

        price = quote["price"]
        cost = price * shares

        user_id = session["user_id"]
        cash = db.execute("SELECT cash from users where id = ?", user_id)[0]["cash"]
        if cost > cash:
            return apology("can not afford")

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?,?,?,?)", user_id, quote["symbol"],shares,price,
        )

        existing = db.execute(
            "SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, quote["symbol"],
        )

        if existing:
            db.execute(
                "UPDATE holdings SET shares = shares + ? WHERE user_id = ? and symbol = ?", shares, user_id, quote["symbol"],
            )
        else:
            db.execute(
                "INSERT INTO holdings (user_id, symbol, shares) VALUES (?,?,?)", user_id, quote["symbol"], shares,
            )

        db.execute("UPDATE users SET cash = cash - ? WHERE id=?", cost, user_id)

        return redirect("/")
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    user_id = session["user_id"]
    rows = db.execute(
        "SELECT symbol, shares, price, ts FROM transactions WHERE user_id = ? ORDER BY ts DESC", user_id,
    )
    return render_template("history.html", rows = rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("missing symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("invalid symbol")
        return render_template("quoted.html", quote=quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
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

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    user_id = session["user_id"]

    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        if not symbol:
            return apology("missing symbol")
        try:
            shares = int(shares)
        except(TypeError, ValueError):
            return apology("shares must be a positive integer")
        if shares <=0:
            return apology("shares must be a positive integer")

        owned = db.execute(
            "SELECT shares FROM holdings WHERE user_id = ? AND symbol = ?", user_id, symbol,
        )

        if not owned or owned[0]["shares"] < shares:
            return apology("too many shares")

        quote = lookup(symbol)
        if not quote:
            return apology("Invalid symbol")

        price = quote["price"]
        proceeds = price * shares

        db.execute(
            "INSERT INTO transactions (user_id, symbol, shares, price) VALUES (?,?,?,?)", user_id, symbol, -shares, price,
        )
        db.execute(
            "UPDATE holdings SET shares = shares - ? WHERE user_id = ? AND symbol = ?", shares, user_id, symbol,
        )

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", proceeds, user_id)

        return redirect("/")
    else:
        symbols = db.execute(
            "SELECT symbol FROM holdings WHERE user_id = ? AND shares > 0 ORDER BY symbol", user_id,
        )
        return render_template("sell.html", symbols=[s["symbol"] for s in symbols])


