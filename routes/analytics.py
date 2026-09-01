# =========================================================
# FOREX TRADING JOURNAL
# routes/analytics.py
# Supabase Analytics Routes
# =========================================================

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session
)

from utils.database import get_db_connection


# =========================================================
# ANALYTICS BLUEPRINT
# =========================================================

analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


# =========================================================
# ANALYTICS HOME
# =========================================================

@analytics_bp.route("/")
def analytics():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    user_id = session["user_id"]

    supabase = get_db_connection()


    # -----------------------------------------------------
    # GET USER TRADES FROM SUPABASE
    # -----------------------------------------------------

    try:

        response = (
            supabase
            .table("trades")
            .select("*")
            .eq("user_id", user_id)
            .order("trade_date", desc=True)
            .execute()
        )

        trades = response.data or []

    except Exception as error:

        print("\n")
        print("=" * 70)
        print("ANALYTICS DATABASE ERROR")
        print("=" * 70)
        print("ERROR:", error)
        print("=" * 70)
        print("\n")

        trades = []


    # -----------------------------------------------------
    # BASIC STATISTICS
    # -----------------------------------------------------

    total_trades = len(trades)

    wins = 0
    losses = 0

    total_profit = 0.0

    best_trade = 0.0
    worst_trade = 0.0


    # -----------------------------------------------------
    # CALCULATE PROFIT / LOSS
    # -----------------------------------------------------

    profits = []

    for trade in trades:

        try:

            profit = float(
                trade.get("profit_loss") or 0
            )

        except (TypeError, ValueError):

            profit = 0.0


        total_profit += profit

        profits.append(profit)


        # -------------------------------------------------
        # WIN / LOSS
        # -------------------------------------------------

        if profit > 0:

            wins += 1

        elif profit < 0:

            losses += 1


    # -----------------------------------------------------
    # BEST / WORST TRADE
    # -----------------------------------------------------

    if profits:

        best_trade = max(profits)

        worst_trade = min(profits)


    # -----------------------------------------------------
    # WIN RATE
    # -----------------------------------------------------

    if total_trades > 0:

        win_rate = round(
            (wins / total_trades) * 100,
            2
        )

    else:

        win_rate = 0


    # -----------------------------------------------------
    # PAIR PERFORMANCE
    # -----------------------------------------------------

    pair_data = {}


    for trade in trades:

        pair = (
            trade.get("pair_name")
            or "Unknown"
        )

        try:

            profit = float(
                trade.get("profit_loss") or 0
            )

        except (TypeError, ValueError):

            profit = 0.0


        # -------------------------------------------------
        # CREATE PAIR
        # -------------------------------------------------

        if pair not in pair_data:

            pair_data[pair] = {
                "trades": 0,
                "wins": 0,
                "losses": 0,
                "profit": 0.0
            }


        # -------------------------------------------------
        # UPDATE PAIR DATA
        # -------------------------------------------------

        pair_data[pair]["trades"] += 1

        pair_data[pair]["profit"] += profit


        if profit > 0:

            pair_data[pair]["wins"] += 1

        elif profit < 0:

            pair_data[pair]["losses"] += 1


    # -----------------------------------------------------
    # RENDER ANALYTICS PAGE
    # -----------------------------------------------------

    return render_template(
        "analytics/analytics.html",

        trades=trades,

        total_trades=total_trades,

        wins=wins,

        losses=losses,

        win_rate=win_rate,

        total_profit=total_profit,

        best_trade=best_trade,

        worst_trade=worst_trade,

        pair_data=pair_data
    )