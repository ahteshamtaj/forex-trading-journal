# =========================================================
# FOREX TRADING JOURNAL
# utils/database.py
# =========================================================

import os
import sqlite3

from config import Config


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():
    """
    Create and return a SQLite database connection.
    """

    database_path = Config.DATABASE

    # Make sure database folder exists
    database_directory = os.path.dirname(
        database_path
    )

    if database_directory:
        os.makedirs(
            database_directory,
            exist_ok=True
        )

    connection = sqlite3.connect(
        database_path,
        timeout=10
    )

    # Return rows like dictionaries
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute(
        "PRAGMA foreign_keys = ON"
    )

    # Better SQLite performance/concurrency
    connection.execute(
        "PRAGMA journal_mode = WAL"
    )

    connection.execute(
        "PRAGMA busy_timeout = 10000"
    )

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():
    """
    Create all required database tables and indexes.
    """

    connection = get_db_connection()

    try:

        cursor = connection.cursor()


        # =================================================
        # USERS TABLE
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                name TEXT NOT NULL,

                email TEXT NOT NULL UNIQUE,

                password TEXT NOT NULL,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP

            )
        """)


        # =================================================
        # TRADES TABLE
        # =================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS trades (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                user_id INTEGER NOT NULL,

                trade_date TEXT NOT NULL,

                pair_name TEXT NOT NULL,

                trade_type TEXT NOT NULL,

                entry_price REAL,

                stop_loss REAL,

                take_profit REAL,

                lot_size REAL,

                risk_reward REAL,

                profit_loss REAL
                    DEFAULT 0,

                strategy TEXT,

                mistake TEXT,

                notes TEXT,

                created_at TIMESTAMP
                    DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id)
                    REFERENCES users(id)
                    ON DELETE CASCADE

            )
        """)


        # =================================================
        # INDEXES
        # =================================================

        # Faster login/email lookup
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_users_email
            ON users(email)
        """)


        # Faster user's trade lookup
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_trades_user_id
            ON trades(user_id)
        """)


        # Faster date-based trade queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_trades_date
            ON trades(trade_date)
        """)


        # User + date queries
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS
            idx_trades_user_date
            ON trades(user_id, trade_date)
        """)


        # =================================================
        # SAVE CHANGES
        # =================================================

        connection.commit()


    except Exception:

        connection.rollback()

        raise


    finally:

        connection.close()