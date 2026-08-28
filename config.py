# =========================================================
# FOREX TRADING JOURNAL
# config.py
# =========================================================

import os


# =========================================================
# BASE DIRECTORY
# =========================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# =========================================================
# CONFIGURATION
# =========================================================

class Config:

    # -----------------------------------------------
    # Environment
    # -----------------------------------------------

    ENV = os.environ.get(
        "APP_ENV",
        "development"
    )


    # -----------------------------------------------
    # Secret Key
    # -----------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY"
    )

    if not SECRET_KEY and ENV != "production":
        SECRET_KEY = "development-only-secret-key"

    if ENV == "production" and not SECRET_KEY:
        raise RuntimeError(
            "SECRET_KEY environment variable is required in production."
        )


    # -----------------------------------------------
    # Database
    # -----------------------------------------------

    DATABASE = os.path.join(
        BASE_DIR,
        "database",
        "trading_journal.db"
    )


    # -----------------------------------------------
    # Session Security
    # -----------------------------------------------

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        ENV == "production"
    )


    # -----------------------------------------------
    # Additional Security
    # -----------------------------------------------

    SESSION_COOKIE_NAME = "forex_journal_session"

    SESSION_REFRESH_EACH_REQUEST = True