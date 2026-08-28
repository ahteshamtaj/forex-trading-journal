# =========================================================
# FOREX TRADING JOURNAL
# routes/profile.py
# =========================================================

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from utils.database import get_db_connection


# =========================================================
# PROFILE BLUEPRINT
# =========================================================

profile_bp = Blueprint(
    "profile",
    __name__
)


# =========================================================
# PROFILE PAGE
# =========================================================

@profile_bp.route("/profile", methods=["GET", "POST"])
def profile():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]

    connection = get_db_connection()


    # -----------------------------------------------------
    # GET USER
    # -----------------------------------------------------

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()


    if user is None:

        connection.close()

        session.clear()

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # UPDATE PROFILE
    # -----------------------------------------------------

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()


        # -------------------------------------------------
        # VALIDATION
        # -------------------------------------------------

        if not name:

            flash(
                "Name cannot be empty.",
                "error"
            )

            connection.close()

            return redirect(
                url_for("profile.profile")
            )


        if not email:

            flash(
                "Email cannot be empty.",
                "error"
            )

            connection.close()

            return redirect(
                url_for("profile.profile")
            )


        # -------------------------------------------------
        # UPDATE USER
        # -------------------------------------------------

        connection.execute(
            """
            UPDATE users
            SET name = ?,
                email = ?
            WHERE id = ?
            """,
            (
                name,
                email,
                user_id
            )
        )

        connection.commit()


        # -------------------------------------------------
        # UPDATE SESSION
        # -------------------------------------------------

        session["user_name"] = name

        session["user_email"] = email


        connection.close()


        flash(
            "Profile updated successfully.",
            "success"
        )


        return redirect(
            url_for("profile.profile")
        )


    # -----------------------------------------------------
    # GET NAME + EMAIL
    # -----------------------------------------------------

    try:
        user_name = user["name"]
    except (KeyError, IndexError):
        user_name = session.get(
            "user_name",
            ""
        )


    try:
        user_email = user["email"]
    except (KeyError, IndexError):
        user_email = session.get(
            "user_email",
            ""
        )


    connection.close()


    # -----------------------------------------------------
    # PROFILE INITIAL
    # -----------------------------------------------------

    profile_initial = (
        user_name[:1].upper()
        if user_name
        else "U"
    )


    return render_template(
        "profile/profile.html",
        user_name=user_name,
        user_email=user_email,
        profile_initial=profile_initial
    )