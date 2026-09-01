# =========================================================
# FOREX TRADING JOURNAL
# utils/database.py
# Supabase Database Connection
# =========================================================

import os

from dotenv import load_dotenv
from supabase import create_client


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

SUPABASE_URL = os.getenv("SUPABASE_URL")

# Backend ke liye SECRET KEY
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")


# =========================================================
# VALIDATE CONFIGURATION
# =========================================================

if not SUPABASE_URL:
    raise RuntimeError(
        "SUPABASE_URL is missing from .env file."
    )

if not SUPABASE_SECRET_KEY:
    raise RuntimeError(
        "SUPABASE_SECRET_KEY is missing from .env file."
    )


# =========================================================
# CREATE SUPABASE CLIENT
# =========================================================

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_SECRET_KEY
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    """
    Return the Supabase client.
    """
    return supabase


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():
    """
    Supabase database is managed from Supabase dashboard.
    """
    return True