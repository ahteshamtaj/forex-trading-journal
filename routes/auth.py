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

    # -----------------------------------------------------
    # ALREADY LOGGED IN
    # -----------------------------------------------------

    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "auth/register.html"
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # VALIDATE NAME
    # -----------------------------------------------------

    if not validate_name(name):

        flash(
            "Please enter a valid name.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # VALIDATE EMAIL
    # -----------------------------------------------------

    if not validate_email(email):

        flash(
            "Please enter a valid email address.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # VALIDATE PASSWORD
    # -----------------------------------------------------

    if not validate_password(password):

        flash(
            "Password must meet the minimum security requirements.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # CONFIRM PASSWORD
    # -----------------------------------------------------

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # TERMS
    # -----------------------------------------------------

    if not terms:

        flash(
            "Please accept the Terms and Privacy Policy.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # CHECK EXISTING USER
    # -----------------------------------------------------

    try:

        existing_user = get_user_by_email(
            email
        )

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("DATABASE ERROR - CHECKING EXISTING USER")
        print("=" * 60)
        print("ERROR:", error)
        print("=" * 60)
        print("\n")

        flash(
            "Unable to connect to the database.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    if existing_user:

        flash(
            "An account with this email already exists.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # HASH PASSWORD
    # -----------------------------------------------------

    hashed_password = generate_password_hash(
        password
    )


    # -----------------------------------------------------
    # CREATE USER
    # -----------------------------------------------------

    try:

        user_id = create_user(
            name,
            email,
            hashed_password
        )

    except Exception as error:

        # IMPORTANT:
        # Show complete error in terminal
        import traceback

        print("\n")
        print("=" * 70)
        print("REGISTER ERROR")
        print("=" * 70)
        print("ERROR:", error)
        print("-" * 70)

        traceback.print_exc()

        print("=" * 70)
        print("\n")

        flash(
            "Something went wrong while creating your account.",
            "error"
        )

        return redirect(
            url_for("auth.register")
        )


    # -----------------------------------------------------
    # AUTO LOGIN
    # -----------------------------------------------------

    session.clear()

    session["user_id"] = user_id

    session["user_name"] = name


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    flash(
        "Account created successfully!",
        "success"
    )

    return redirect(
        url_for("dashboard.dashboard")
    )


# =========================================================
# LOGIN
# =========================================================

@auth_bp.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    # -----------------------------------------------------
    # ALREADY LOGGED IN
    # -----------------------------------------------------

    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "auth/login.html"
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    email = request.form.get(
        "email",
        ""
    ).strip().lower()

    password = request.form.get(
        "password",
        ""
    )


    # -----------------------------------------------------
    # EMPTY FIELDS
    # -----------------------------------------------------

    if not email or not password:

        flash(
            "Please enter your email and password.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # GET USER
    # -----------------------------------------------------

    try:

        user = get_user_by_email(
            email
        )

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("LOGIN DATABASE ERROR")
        print("=" * 60)
        print("ERROR:", error)
        print("=" * 60)
        print("\n")

        flash(
            "Unable to connect to the database.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # USER NOT FOUND
    # -----------------------------------------------------

    if user is None:

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # CHECK PASSWORD
    # -----------------------------------------------------

    try:

        password_valid = check_password_hash(
            user["password"],
            password
        )

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("PASSWORD CHECK ERROR")
        print("=" * 60)
        print("ERROR:", error)
        print("=" * 60)
        print("\n")

        flash(
            "Unable to verify your password.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    if not password_valid:

        flash(
            "Invalid email or password.",
            "error"
        )

        return redirect(
            url_for("auth.login")
        )


    # -----------------------------------------------------
    # CREATE SESSION
    # -----------------------------------------------------

    session.clear()

    session["user_id"] = user["id"]

    session["user_name"] = user["name"]


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    flash(
        "Welcome back!",
        "success"
    )

    return redirect(
        url_for("dashboard.dashboard")
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

    # -----------------------------------------------------
    # ALREADY LOGGED IN
    # -----------------------------------------------------

    if session.get("user_id"):

        return redirect(
            url_for("dashboard.dashboard")
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "auth/forgot_password.html"
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    email = request.form.get(
        "email",
        ""
    ).strip().lower()


    # -----------------------------------------------------
    # VALIDATE EMAIL
    # -----------------------------------------------------

    if not validate_email(email):

        flash(
            "Please enter a valid email address.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )


    # -----------------------------------------------------
    # FIND USER
    # -----------------------------------------------------

    try:

        user = get_user_by_email(
            email
        )

    except Exception as error:

        print("\n")
        print("=" * 60)
        print("FORGOT PASSWORD DATABASE ERROR")
        print("=" * 60)
        print("ERROR:", error)
        print("=" * 60)
        print("\n")

        flash(
            "Unable to connect to the database.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )


    if user is None:

        flash(
            "No account was found with this email.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )


    # -----------------------------------------------------
    # PASSWORD RESET SESSION
    # -----------------------------------------------------

    session["password_reset_user_id"] = user["id"]

    session["password_reset_email"] = user["email"]


    # -----------------------------------------------------
    # RESET PASSWORD
    # -----------------------------------------------------

    return redirect(
        url_for("auth.reset_password")
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


    # -----------------------------------------------------
    # NO RESET SESSION
    # -----------------------------------------------------

    if not user_id:

        flash(
            "Please start the password reset process again.",
            "error"
        )

        return redirect(
            url_for("auth.forgot_password")
        )


    # -----------------------------------------------------
    # GET
    # -----------------------------------------------------

    if request.method == "GET":

        return render_template(
            "auth/reset_password.html"
        )


    # -----------------------------------------------------
    # POST
    # -----------------------------------------------------

    password = request.form.get(
        "password",
        ""
    )

    confirm_password = request.form.get(
        "confirm_password",
        ""
    )


    # -----------------------------------------------------
    # VALIDATE PASSWORD
    # -----------------------------------------------------

    if not validate_password(password):

        flash(
            "Password must meet the minimum security requirements.",
            "error"
        )

        return redirect(
            url_for("auth.reset_password")
        )


    # -----------------------------------------------------
    # CONFIRM PASSWORD
    # -----------------------------------------------------

    if password != confirm_password:

        flash(
            "Passwords do not match.",
            "error"
        )

        return redirect(
            url_for("auth.reset_password")
        )


    # -----------------------------------------------------
    # HASH PASSWORD
    # -----------------------------------------------------

    hashed_password = generate_password_hash(
        password
    )


    # -----------------------------------------------------
    # UPDATE PASSWORD
    # -----------------------------------------------------

    try:

        update_user_password(
            user_id,
            hashed_password
        )

    except Exception as error:

        import traceback

        print("\n")
        print("=" * 70)
        print("PASSWORD RESET ERROR")
        print("=" * 70)
        print("ERROR:", error)
        print("-" * 70)

        traceback.print_exc()

        print("=" * 70)
        print("\n")

        flash(
            "Unable to update your password. Please try again.",
            "error"
        )

        return redirect(
            url_for("auth.reset_password")
        )


    # -----------------------------------------------------
    # CLEAR RESET SESSION
    # -----------------------------------------------------

    session.pop(
        "password_reset_user_id",
        None
    )

    session.pop(
        "password_reset_email",
        None
    )


    # -----------------------------------------------------
    # SUCCESS
    # -----------------------------------------------------

    flash(
        "Password reset successfully. You can now login.",
        "success"
    )

    return redirect(
        url_for("auth.login")
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