# =========================================================
# FOREX TRADING JOURNAL
# routes/auth.py
# Authentication Routes
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

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from models.user import (
    get_user_by_email,
    create_user,
    update_user_password
)

from utils.validators import (
    validate_email,
    validate_password,
    validate_name
)


# =========================================================
# AUTH BLUEPRINT
# =========================================================

auth_bp = Blueprint(
    "auth",
    __name__
)


# =========================================================
# REGISTER
# =========================================================

@auth_bp.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    # Already logged in
    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )

    # POST
    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        terms = request.form.get(
            "terms"
        )

        # -----------------------------------------
        # Validate Name
        # -----------------------------------------

        if not validate_name(name):

            flash(
                "Please enter a valid name.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Validate Email
        # -----------------------------------------

        if not validate_email(email):

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Validate Password
        # -----------------------------------------

        if not validate_password(password):

            flash(
                "Password must meet the minimum security requirements.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Confirm Password
        # -----------------------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Terms
        # -----------------------------------------

        if not terms:

            flash(
                "Please accept the Terms and Privacy Policy.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Existing User
        # -----------------------------------------

        existing_user = get_user_by_email(
            email
        )

        if existing_user:

            flash(
                "An account with this email already exists.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Hash Password
        # -----------------------------------------

        hashed_password = generate_password_hash(
            password
        )

        # -----------------------------------------
        # Create User
        # -----------------------------------------

        try:

            user_id = create_user(
                name,
                email,
                hashed_password
            )

        except Exception as error:

            print("REGISTER ERROR:", error)

            flash(
                "Something went wrong while creating your account.",
                "error"
            )

            return redirect(
                url_for("auth.register")
            )

        # -----------------------------------------
        # Login Automatically
        # -----------------------------------------

        session.clear()

        session["user_id"] = user_id

        session["user_name"] = name

        flash(
            "Account created successfully!",
            "success"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    # GET
    return render_template(
        "auth/register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # Already logged in
    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )

    # POST
    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        # -----------------------------------------
        # Empty Fields
        # -----------------------------------------

        if not email or not password:

            flash(
                "Please enter your email and password.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        # -----------------------------------------
        # Find User
        # -----------------------------------------

        user = get_user_by_email(
            email
        )

        # -----------------------------------------
        # User Not Found
        # -----------------------------------------

        if user is None:

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        # -----------------------------------------
        # Check Password
        # -----------------------------------------

        if not check_password_hash(
            user["password"],
            password
        ):

            flash(
                "Invalid email or password.",
                "error"
            )

            return redirect(
                url_for("auth.login")
            )

        # -----------------------------------------
        # Create Session
        # -----------------------------------------

        session.clear()

        session["user_id"] = user["id"]

        session["user_name"] = user["name"]

        flash(
            "Welcome back!",
            "success"
        )

        return redirect(
            url_for("dashboard.dashboard")
        )

    # GET
    return render_template(
        "auth/login.html"
    )


# =========================================================
# FORGOT PASSWORD
# =========================================================

@auth_bp.route(
    "/forgot-password",
    methods=["GET", "POST"]
)
@auth_bp.route(
    "/forgot_password",
    methods=["GET", "POST"]
)
def forgot_password():

    # Already logged in
    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )

    # -----------------------------------------
    # POST
    # -----------------------------------------

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        # -------------------------------------
        # Validate Email
        # -------------------------------------

        if not validate_email(email):

            flash(
                "Please enter a valid email address.",
                "error"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        # -------------------------------------
        # Find User
        # -------------------------------------

        user = get_user_by_email(
            email
        )

        if user is None:

            flash(
                "No account was found with this email.",
                "error"
            )

            return redirect(
                url_for("auth.forgot_password")
            )

        # -------------------------------------
        # Temporary Reset Session
        # -------------------------------------

        session["password_reset_user_id"] = user["id"]

        session["password_reset_email"] = user["email"]

        # -------------------------------------
        # Go To Reset Password
        # -------------------------------------

        return redirect(
            url_for("auth.reset_password")
        )

    # -----------------------------------------
    # GET
    # -----------------------------------------

    return render_template(
        "auth/forgot_password.html"
    )


# =========================================================
# RESET PASSWORD
# =========================================================

@auth_bp.route(
    "/reset-password",
    methods=["GET", "POST"]
)
@auth_bp.route(
    "/reset_password",
    methods=["GET", "POST"]
)
def reset_password():

    user_id = session.get(
        "password_reset_user_id"
    )

    # -----------------------------------------
    # No Reset Session
    # -----------------------------------------

    if not user_id:

        flash(
            "Please start the password reset process again.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )

    # -----------------------------------------
    # POST
    # -----------------------------------------

    if request.method == "POST":

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        # -------------------------------------
        # Validate Password
        # -------------------------------------

        if not validate_password(password):

            flash(
                "Password must meet the minimum security requirements.",
                "error"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        # -------------------------------------
        # Confirm Password
        # -------------------------------------

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        # -------------------------------------
        # Hash New Password
        # -------------------------------------

        hashed_password = generate_password_hash(
            password
        )

        # -------------------------------------
        # Update Password
        # -------------------------------------

        try:

            update_user_password(
                user_id,
                hashed_password
            )

        except Exception as error:

            print("PASSWORD RESET ERROR:", error)

            flash(
                "Unable to update your password. Please try again.",
                "error"
            )

            return redirect(
                url_for("auth.reset_password")
            )

        # -------------------------------------
        # Clear Reset Session
        # -------------------------------------

        session.pop(
            "password_reset_user_id",
            None
        )

        session.pop(
            "password_reset_email",
            None
        )

        # -------------------------------------
        # Success
        # -------------------------------------

        flash(
            "Password reset successfully. You can now login.",
            "success"
        )

        return redirect(
            url_for("auth.login")
        )

    # -----------------------------------------
    # GET
    # -----------------------------------------

    return render_template(
        "auth/reset_password.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@auth_bp.route(
    "/logout"
)
def logout():

    session.clear()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )