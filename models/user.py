# =========================================================
# FOREX TRADING JOURNAL
# models/user.py
# =========================================================

from utils.database import get_db_connection


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    ).fetchone()

    connection.close()

    return user


# =========================================================
# GET USER BY ID
# =========================================================

def get_user_by_id(user_id):

    connection = get_db_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE id = ?
        """,
        (user_id,)
    ).fetchone()

    connection.close()

    return user


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    name,
    email,
    password
):

    connection = get_db_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO users
        (
            name,
            email,
            password
        )
        VALUES (?, ?, ?)
        """,
        (
            name,
            email,
            password
        )
    )

    connection.commit()

    user_id = cursor.lastrowid

    connection.close()

    return user_id


# =========================================================
# UPDATE USER PASSWORD
# =========================================================

def update_user_password(
    user_id,
    hashed_password
):

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE users
        SET password = ?
        WHERE id = ?
        """,
        (
            hashed_password,
            user_id
        )
    )

    connection.commit()

    connection.close()