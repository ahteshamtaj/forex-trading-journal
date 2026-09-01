# =========================================================
# FOREX TRADING JOURNAL
# config.py
# =========================================================

import os
from dotenv import load_dotenv


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


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

    # -----------------------------------------------------
    # Environment
    # -----------------------------------------------------

    ENV = os.environ.get(
        "APP_ENV",
        "development"
    )


    # -----------------------------------------------------
    # Flask Secret Key
    # -----------------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY"
    )

    if not SECRET_KEY:
        SECRET_KEY = "development-only-secret-key"


    # -----------------------------------------------------
    # Supabase
    # -----------------------------------------------------

    SUPABASE_URL = os.environ.get(
        "SUPABASE_URL"
    )

    SUPABASE_PUBLISHABLE_KEY = os.environ.get(
        "SUPABASE_PUBLISHABLE_KEY"
    )


    # -----------------------------------------------------
    # Validate Supabase Configuration
    # -----------------------------------------------------

    if not SUPABASE_URL:
        raise RuntimeError(
            "SUPABASE_URL is missing from .env"
        )

    if not SUPABASE_PUBLISHABLE_KEY:
        raise RuntimeError(
            "SUPABASE_PUBLISHABLE_KEY is missing from .env"
        )


    # -----------------------------------------------------
    # Local Database
    # -----------------------------------------------------

    DATABASE = os.path.join(
        BASE_DIR,
        "database",
        "trading_journal.db"
    )


    # -----------------------------------------------------
    # Session Security
    # -----------------------------------------------------

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = (
        ENV == "production"
    )

    SESSION_COOKIE_NAME = (
        "forex_journal_session"
    )

    SESSION_REFRESH_EACH_REQUEST = True


# =========================================================
# END OF CONFIG
# =========================================================