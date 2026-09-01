# =========================================================
# FOREX TRADING JOURNAL
# models/user.py
# Supabase User Model
# =========================================================

from utils.database import get_db_connection


# =========================================================
# GET USER BY EMAIL
# =========================================================

def get_user_by_email(email):

    supabase = get_db_connection()

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("email", email)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# =========================================================
# GET USER BY ID
# =========================================================

def get_user_by_id(user_id):

    supabase = get_db_connection()

    response = (
        supabase
        .table("users")
        .select("*")
        .eq("id", user_id)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# =========================================================
# CREATE USER
# =========================================================

def create_user(
    name,
    email,
    password
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("users")
        .insert({
            "name": name,
            "email": email,
            "password": password
        })
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "User was not created in Supabase."
        )

    return response.data[0]["id"]


# =========================================================
# UPDATE USER PASSWORD
# =========================================================

def update_user_password(
    user_id,
    hashed_password
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("users")
        .update({
            "password": hashed_password
        })
        .eq("id", user_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Password was not updated."
        )

    return True