# =========================================================
# FOREX TRADING JOURNAL
# routes/journal.py
# Journal Routes
# =========================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from models.trade import (
    create_trade,
    get_user_trades,
    get_trade_by_id,
    update_trade,
    delete_trade
)


# =========================================================
# JOURNAL BLUEPRINT
# =========================================================

journal_bp = Blueprint(
    "journal",
    __name__,
    url_prefix="/journal"
)


# =========================================================
# JOURNAL HOME
# =========================================================

@journal_bp.route("/")
def journal():

    # -----------------------------------------
    # LOGIN CHECK
    # -----------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    # -----------------------------------------
    # GET USER TRADES
    # -----------------------------------------

    trades = get_user_trades(
        session["user_id"]
    )

    return render_template(
        "journal/journal.html",
        trades=trades
    )


# =========================================================
# ADD TRADE
# =========================================================

@journal_bp.route(
    "/add",
    methods=["GET", "POST"]
)
def add_trade():

    # -----------------------------------------
    # LOGIN CHECK
    # -----------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )

    # -----------------------------------------
    # POST
    # -----------------------------------------

    if request.method == "POST":

        # -----------------------------------------
        # GET FORM DATA
        # -----------------------------------------

        trade_date = request.form.get(
            "trade_date",
            ""
        ).strip()

        pair_name = request.form.get(
            "pair_name",
            ""
        ).strip()

        trade_type = request.form.get(
            "trade_type",
            ""
        ).strip()

        lot_size = request.form.get(
            "lot_size",
            ""
        ).strip()

        profit_loss = request.form.get(
            "profit_loss",
            "0"
        ).strip()

        mistake = request.form.get(
            "mistake",
            ""
        ).strip()


        # -----------------------------------------
        # REQUIRED FIELDS
        # -----------------------------------------

        if not trade_date:

            flash(
                "Please enter the trade date.",
                "error"
            )

            return redirect(
                url_for("journal.add_trade")
            )


        if not pair_name:

            flash(
                "Please enter the trading pair.",
                "error"
            )

            return redirect(
                url_for("journal.add_trade")
            )


        if not trade_type:

            flash(
                "Please select the trade type.",
                "error"
            )

            return redirect(
                url_for("journal.add_trade")
            )


        # -----------------------------------------
        # CONVERT NUMERIC VALUES
        # -----------------------------------------

        try:

            lot_size = (
                float(lot_size)
                if lot_size
                else None
            )

            profit_loss = (
                float(profit_loss)
                if profit_loss
                else 0
            )

        except ValueError:

            flash(
                "Please enter valid numeric values.",
                "error"
            )

            return redirect(
                url_for("journal.add_trade")
            )


        # -----------------------------------------
        # CREATE TRADE
        # -----------------------------------------

        try:

            create_trade(

                session["user_id"],

                trade_date,
                pair_name,
                trade_type,

                lot_size,
                profit_loss,

                mistake
            )

        except Exception as error:

            print(
                "ADD TRADE ERROR:",
                error
            )

            flash(
                "Unable to save the trade. Please try again.",
                "error"
            )

            return redirect(
                url_for("journal.add_trade")
            )


        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        flash(
            "Trade added successfully.",
            "success"
        )

        return redirect(
            url_for("journal.journal")
        )


    # -----------------------------------------
    # GET
    # -----------------------------------------

    return render_template(
        "journal/add_trade.html"
    )


# =========================================================
# EDIT TRADE
# =========================================================

@journal_bp.route(
    "/edit/<int:trade_id>",
    methods=["GET", "POST"]
)
def edit_trade(trade_id):

    # -----------------------------------------
    # LOGIN CHECK
    # -----------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------
    # GET EXISTING TRADE
    # -----------------------------------------

    trade = get_trade_by_id(
        trade_id,
        session["user_id"]
    )


    if trade is None:

        flash(
            "Trade not found.",
            "error"
        )

        return redirect(
            url_for("journal.journal")
        )


    # -----------------------------------------
    # POST UPDATE
    # -----------------------------------------

    if request.method == "POST":

        trade_date = request.form.get(
            "trade_date",
            ""
        ).strip()

        pair_name = request.form.get(
            "pair_name",
            ""
        ).strip()

        trade_type = request.form.get(
            "trade_type",
            ""
        ).strip()

        lot_size = request.form.get(
            "lot_size",
            ""
        ).strip()

        profit_loss = request.form.get(
            "profit_loss",
            "0"
        ).strip()

        mistake = request.form.get(
            "mistake",
            ""
        ).strip()


        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not trade_date:

            flash(
                "Please enter the trade date.",
                "error"
            )

            return redirect(
                url_for(
                    "journal.edit_trade",
                    trade_id=trade_id
                )
            )


        if not pair_name:

            flash(
                "Please enter the trading pair.",
                "error"
            )

            return redirect(
                url_for(
                    "journal.edit_trade",
                    trade_id=trade_id
                )
            )


        if not trade_type:

            flash(
                "Please select the trade type.",
                "error"
            )

            return redirect(
                url_for(
                    "journal.edit_trade",
                    trade_id=trade_id
                )
            )


        # -----------------------------------------
        # CONVERT NUMERIC VALUES
        # -----------------------------------------

        try:

            lot_size = (
                float(lot_size)
                if lot_size
                else None
            )

            profit_loss = (
                float(profit_loss)
                if profit_loss
                else 0
            )

        except ValueError:

            flash(
                "Please enter valid numeric values.",
                "error"
            )

            return redirect(
                url_for(
                    "journal.edit_trade",
                    trade_id=trade_id
                )
            )


        # -----------------------------------------
        # UPDATE TRADE
        # -----------------------------------------

        try:

            update_trade(

                trade_id,
                session["user_id"],

                trade_date,
                pair_name,
                trade_type,

                lot_size,
                profit_loss,

                mistake
            )

        except Exception as error:

            print(
                "UPDATE TRADE ERROR:",
                error
            )

            flash(
                "Unable to update the trade. Please try again.",
                "error"
            )

            return redirect(
                url_for(
                    "journal.edit_trade",
                    trade_id=trade_id
                )
            )


        # -----------------------------------------
        # SUCCESS
        # -----------------------------------------

        flash(
            "Trade updated successfully.",
            "success"
        )

        return redirect(
            url_for("journal.journal")
        )


    # -----------------------------------------
    # EDIT PAGE
    # -----------------------------------------

    return render_template(
        "journal/edit_trade.html",
        trade=trade
    )


# =========================================================
# DELETE TRADE
# =========================================================

@journal_bp.route(
    "/delete/<int:trade_id>",
    methods=["POST"]
)
def delete(trade_id):

    # -----------------------------------------
    # LOGIN CHECK
    # -----------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------
    # VERIFY OWNERSHIP
    # -----------------------------------------

    trade = get_trade_by_id(
        trade_id,
        session["user_id"]
    )


    if trade is None:

        flash(
            "Trade not found.",
            "error"
        )

        return redirect(
            url_for("journal.journal")
        )


    # -----------------------------------------
    # DELETE
    # -----------------------------------------

    try:

        delete_trade(
            trade_id,
            session["user_id"]
        )

    except Exception as error:

        print(
            "DELETE TRADE ERROR:",
            error
        )

        flash(
            "Unable to delete the trade.",
            "error"
        )

        return redirect(
            url_for("journal.journal")
        )


    # -----------------------------------------
    # SUCCESS
    # -----------------------------------------

    flash(
        "Trade deleted successfully.",
        "success"
    )

    return redirect(
        url_for("journal.journal")
    )