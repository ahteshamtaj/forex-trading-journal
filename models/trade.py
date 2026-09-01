# =========================================================
# FOREX TRADING JOURNAL
# models/trade.py
# Supabase Trade Model
# =========================================================

from utils.database import get_db_connection


# =========================================================
# CREATE TRADE
# =========================================================

def create_trade(
    user_id,
    trade_date,
    pair_name,
    trade_type,
    lot_size,
    profit_loss,
    mistake
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("trades")
        .insert({
            "user_id": user_id,
            "trade_date": trade_date,
            "pair_name": pair_name,
            "trade_type": trade_type,
            "lot_size": lot_size,
            "profit_loss": profit_loss,
            "mistake": mistake
        })
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Trade could not be created."
        )

    return response.data[0]


# =========================================================
# GET USER TRADES
# =========================================================

def get_user_trades(user_id):

    supabase = get_db_connection()

    response = (
        supabase
        .table("trades")
        .select("*")
        .eq("user_id", user_id)
        .order("trade_date", desc=True)
        .execute()
    )

    return response.data


# =========================================================
# GET SINGLE TRADE
# =========================================================

def get_trade_by_id(
    trade_id,
    user_id
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("trades")
        .select("*")
        .eq("id", trade_id)
        .eq("user_id", user_id)
        .limit(1)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


# =========================================================
# UPDATE TRADE
# =========================================================

def update_trade(
    trade_id,
    user_id,
    trade_date,
    pair_name,
    trade_type,
    lot_size,
    profit_loss,
    mistake
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("trades")
        .update({
            "trade_date": trade_date,
            "pair_name": pair_name,
            "trade_type": trade_type,
            "lot_size": lot_size,
            "profit_loss": profit_loss,
            "mistake": mistake
        })
        .eq("id", trade_id)
        .eq("user_id", user_id)
        .execute()
    )

    if not response.data:
        raise RuntimeError(
            "Trade could not be updated."
        )

    return response.data[0]


# =========================================================
# DELETE TRADE
# =========================================================

def delete_trade(
    trade_id,
    user_id
):

    supabase = get_db_connection()

    response = (
        supabase
        .table("trades")
        .delete()
        .eq("id", trade_id)
        .eq("user_id", user_id)
        .execute()
    )

    return True