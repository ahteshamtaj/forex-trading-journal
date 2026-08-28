# =========================================================
# FOREX TRADING JOURNAL
# utils/validators.py
# =========================================================

import re


# =========================================================
# NAME VALIDATION
# =========================================================

def validate_name(name):
    """
    Validate user's name.

    Requirements:
    - Must be a string
    - Minimum 2 characters
    - Maximum 80 characters
    - Letters, spaces, apostrophes and hyphens allowed
    """

    if not isinstance(name, str):
        return False

    name = name.strip()

    if len(name) < 2:
        return False

    if len(name) > 80:
        return False

    # Allows names such as:
    # Ahtesham Ahmad
    # Ahtesham-Ahmad
    # O'Connor
    if not re.fullmatch(
        r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ\s'\-]*",
        name
    ):
        return False

    return True


# =========================================================
# EMAIL VALIDATION
# =========================================================

def validate_email(email):
    """
    Validate email address.
    """

    if not isinstance(email, str):
        return False

    email = email.strip().lower()

    if len(email) > 254:
        return False

    email_pattern = re.compile(
        r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@"
        r"[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?"
        r"(?:\.[A-Za-z0-9]"
        r"(?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)+$"
    )

    return bool(
        email_pattern.fullmatch(email)
    )


# =========================================================
# PASSWORD VALIDATION
# =========================================================

def validate_password(password):
    """
    Validate password strength.

    Requirements:
    - At least 8 characters
    - Maximum 128 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    """

    if not isinstance(password, str):
        return False

    if len(password) < 8:
        return False

    if len(password) > 128:
        return False

    if not re.search(r"[A-Z]", password):
        return False

    if not re.search(r"[a-z]", password):
        return False

    if not re.search(r"[0-9]", password):
        return False

    return True


# =========================================================
# TRADE PAIR VALIDATION
# =========================================================

def validate_pair(pair_name):
    """
    Validate forex pair name.

    Examples:
    EURUSD
    GBPUSD
    XAUUSD
    USDJPY
    """

    if not isinstance(pair_name, str):
        return False

    pair_name = pair_name.strip().upper()

    if not pair_name:
        return False

    if len(pair_name) > 20:
        return False

    return bool(
        re.fullmatch(
            r"[A-Z0-9._-]+",
            pair_name
        )
    )


# =========================================================
# TRADE TYPE VALIDATION
# =========================================================

def validate_trade_type(trade_type):
    """
    Validate trade direction.
    """

    if not isinstance(trade_type, str):
        return False

    return trade_type.strip().lower() in {
        "buy",
        "sell",
        "long",
        "short"
    }


# =========================================================
# NUMBER VALIDATION
# =========================================================

def validate_number(value):
    """
    Validate numeric values such as:
    - Entry price
    - Stop loss
    - Take profit
    - Lot size
    - Risk reward
    - Profit / Loss
    """

    try:

        number = float(value)

    except (
        TypeError,
        ValueError
    ):

        return False

    return number == number and number not in (
        float("inf"),
        float("-inf")
    )


# =========================================================
# TEXT VALIDATION
# =========================================================

def validate_text(
    text,
    min_length=0,
    max_length=5000
):
    """
    Validate general text fields.
    """

    if text is None:
        return False

    if not isinstance(text, str):
        return False

    text = text.strip()

    if len(text) < min_length:
        return False

    if len(text) > max_length:
        return False

    return True