# =========================================================
# FOREX TRADING JOURNAL
# routes/profile.py
# Supabase Profile Routes
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

@profile_bp.route(
    "/profile",
    methods=["GET", "POST"]
)
def profile():

    # -----------------------------------------------------
    # LOGIN CHECK
    # -----------------------------------------------------

    if "user_id" not in session:

        return redirect(
            url_for("auth.login")
        )


    user_id = session["user_id"]

    supabase = get_db_connection()


    # =====================================================
    # GET USER
    # =====================================================

    try:

        response = (
            supabase
            .table("users")
            .select("*")
            .eq("id", user_id)
            .limit(1)
            .execute()
        )

        users = response.data or []

    except Exception as error:

        print("\n")
        print("=" * 70)
        print("PROFILE DATABASE ERROR")
        print("=" * 70)
        print("ERROR:", error)
        print("=" * 70)
        print("\n")

        flash(
            "Unable to connect to the database.",
            "error"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )


    # -----------------------------------------------------
    # USER NOT FOUND
    # -----------------------------------------------------

    if not users:

        session.clear()

        flash(
            "User account was not found.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    user = users[0]


    # =====================================================
    # UPDATE PROFILE
    # =====================================================

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()


        # -------------------------------------------------
        # NAME VALIDATION
        # -------------------------------------------------

        if not name:

            flash(
                "Name cannot be empty.",
                "error"
            )

            return redirect(
                url_for("profile.profile")
            )


        # -------------------------------------------------
        # EMAIL VALIDATION
        # -------------------------------------------------

        if not email:

            flash(
                "Email cannot be empty.",
                "error"
            )

            return redirect(
                url_for("profile.profile")
            )


        # =================================================
        # UPDATE USER IN SUPABASE
        # =================================================

        try:

            response = (
                supabase
                .table("users")
                .update({
                    "name": name,
                    "email": email
                })
                .eq("id", user_id)
                .execute()
            )


            # -------------------------------------------------
            # CHECK UPDATE RESULT
            # -------------------------------------------------

            if not response.data:

                flash(
                    "Profile could not be updated.",
                    "error"
                )

                return redirect(
                    url_for("profile.profile")
                )


        except Exception as error:

            print("\n")
            print("=" * 70)
            print("PROFILE UPDATE ERROR")
            print("=" * 70)
            print("ERROR:", error)
            print("=" * 70)
            print("\n")

            flash(
                "Unable to update your profile.",
                "error"
            )

            return redirect(
                url_for("profile.profile")
            )


        # -------------------------------------------------
        # UPDATE SESSION
        # -------------------------------------------------

        session["user_name"] = name

        session["user_email"] = email


        # -------------------------------------------------
        # SUCCESS
        # -------------------------------------------------

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("profile.profile")
        )


    # =====================================================
    # GET NAME + EMAIL
    # =====================================================

    user_name = user.get(
        "name",
        session.get(
            "user_name",
            ""
        )
    )


    user_email = user.get(
        "email",
        session.get(
            "user_email",
            ""
        )
    )


    # =====================================================
    # PROFILE INITIAL
    # =====================================================

    profile_initial = (
        user_name[:1].upper()
        if user_name
        else "U"
    )


    # =====================================================
    # RENDER PROFILE
    # =====================================================

    return render_template(
        "profile/profile.html",

        user_name=user_name,

        user_email=user_email,

        profile_initial=profile_initial
    )