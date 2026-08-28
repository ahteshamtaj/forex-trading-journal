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

    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO trades (
            user_id,
            trade_date,
            pair_name,
            trade_type,
            lot_size,
            profit_loss,
            mistake
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            user_id,
            trade_date,
            pair_name,
            trade_type,
            lot_size,
            profit_loss,
            mistake
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# GET USER TRADES
# =========================================================

def get_user_trades(user_id):

    connection = get_db_connection()

    trades = connection.execute(
        """
        SELECT *
        FROM trades
        WHERE user_id = ?
        ORDER BY trade_date DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return trades


# =========================================================
# GET SINGLE TRADE
# =========================================================

def get_trade_by_id(trade_id, user_id):

    connection = get_db_connection()

    trade = connection.execute(
        """
        SELECT *
        FROM trades
        WHERE id = ?
        AND user_id = ?
        """,
        (trade_id, user_id)
    ).fetchone()

    connection.close()

    return trade


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

    connection = get_db_connection()

    connection.execute(
        """
        UPDATE trades
        SET
            trade_date = ?,
            pair_name = ?,
            trade_type = ?,
            lot_size = ?,
            profit_loss = ?,
            mistake = ?
        WHERE id = ?
        AND user_id = ?
        """,
        (
            trade_date,
            pair_name,
            trade_type,
            lot_size,
            profit_loss,
            mistake,
            trade_id,
            user_id
        )
    )

    connection.commit()
    connection.close()


# =========================================================
# DELETE TRADE
# =========================================================

def delete_trade(trade_id, user_id):

    connection = get_db_connection()

    connection.execute(
        """
        DELETE FROM trades
        WHERE id = ?
        AND user_id = ?
        """,
        (trade_id, user_id)
    )

    connection.commit()
    connection.close()