# =========================================================
# FOREX TRADING JOURNAL
# routes/dashboard.py
# Dashboard & Analytics Routes
# =========================================================

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from models.trade import get_user_trades


# =========================================================
# DASHBOARD BLUEPRINT
# =========================================================

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


# =========================================================
# DASHBOARD
# =========================================================

@dashboard_bp.route("/dashboard")
def dashboard():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # GET USER TRADES
    # -----------------------------------------------------

    trades = get_user_trades(
        session["user_id"]
    )


    # -----------------------------------------------------
    # CALCULATE STATISTICS
    # -----------------------------------------------------

    total_trades = len(trades)

    wins = 0
    losses = 0
    total_profit = 0.0


    for trade in trades:

        profit = float(
            trade["profit_loss"] or 0
        )

        total_profit += profit


        if profit > 0:

            wins += 1

        elif profit < 0:

            losses += 1


    # -----------------------------------------------------
    # WIN RATE
    # -----------------------------------------------------

    win_rate = 0

    if total_trades > 0:

        win_rate = round(
            (wins / total_trades) * 100,
            2
        )


    # -----------------------------------------------------
    # RENDER DASHBOARD
    # -----------------------------------------------------

    return render_template(
        "dashboard/dashboard.html",

        trades=trades,

        total_trades=total_trades,

        wins=wins,

        losses=losses,

        total_profit=total_profit,

        win_rate=win_rate
    )


# =========================================================
# ANALYTICS
# =========================================================

@dashboard_bp.route("/analytics")
def analytics():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # GET USER TRADES
    # -----------------------------------------------------

    trades = get_user_trades(
        session["user_id"]
    )


    # -----------------------------------------------------
    # CALCULATE STATISTICS
    # -----------------------------------------------------

    total_trades = len(trades)

    wins = 0
    losses = 0
    total_profit = 0.0


    for trade in trades:

        profit = float(
            trade["profit_loss"] or 0
        )

        total_profit += profit


        if profit > 0:

            wins += 1

        elif profit < 0:

            losses += 1


    # -----------------------------------------------------
    # WIN RATE
    # -----------------------------------------------------

    win_rate = 0

    if total_trades > 0:

        win_rate = round(
            (wins / total_trades) * 100,
            2
        )


    # -----------------------------------------------------
    # RENDER ANALYTICS
    # -----------------------------------------------------

    return render_template(
        "dashboard/analytics.html",

        trades=trades,

        total_trades=total_trades,

        wins=wins,

        losses=losses,

        total_profit=total_profit,

        win_rate=win_rate
    )