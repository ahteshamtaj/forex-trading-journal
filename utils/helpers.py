# =========================================================
# FOREX TRADING JOURNAL
# utils/helpers.py
# =========================================================

from itsdangerous import URLSafeTimedSerializer

from flask import current_app


# =========================================================
# CREATE PASSWORD RESET TOKEN
# =========================================================

def generate_reset_token(email):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    return serializer.dumps(
        email,
        salt="password-reset"
    )


# =========================================================
# VERIFY PASSWORD RESET TOKEN
# =========================================================

def verify_reset_token(token, max_age=1800):

    serializer = URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"]
    )

    try:

        email = serializer.loads(
            token,
            salt="password-reset",
            max_age=max_age
        )

        return email

    except Exception:

        return None