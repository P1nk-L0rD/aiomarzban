import datetime


def current_unix_utc_time() -> int:
    """
    Return the current UTC time as a Unix timestamp (seconds since epoch).
    """
    utc_now = datetime.datetime.now(tz=datetime.timezone.utc)
    return int(utc_now.timestamp())


def future_unix_time(days: int = 0, hours: int = 0, minutes: int = 0) -> int:
    """
    Return the unix time in seconds since epoch.
    """

    now_time = datetime.datetime.now(tz=datetime.timezone.utc)
    future_time = now_time + datetime.timedelta(days=days, hours=hours, minutes=minutes)
    return int(future_time.timestamp())


def unix_time_delta(days: int = 0, hours: int = 0, minutes: int = 0) -> int:
    """
    Return the unix time delta.
    """
    return int(datetime.timedelta(days=days, hours=hours, minutes=minutes).total_seconds())


def gb_to_bytes(amount_of_gb: int) -> int:
    if amount_of_gb:
        return amount_of_gb * 1024 ** 3
    return amount_of_gb


def bytes_to_gb(amount_of_bytes: int) -> int:
    if amount_of_bytes:
        return round(amount_of_bytes / (1024 ** 3), 2)
    return amount_of_bytes
