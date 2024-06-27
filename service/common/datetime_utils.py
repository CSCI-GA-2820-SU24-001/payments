from datetime import datetime
# Standardized datetime format
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime_from_str(datetime_str: str) -> datetime:
    """Converts a string of a datetime into a Datetime object

    Args:
        datetime_str (str): a string representation of a datetime

    Raises:
        ValueError: If the string representation does not match a valid datetime format

    Returns:
        datetime: a datetime object
    """
    formats = [DATETIME_FORMAT, "%Y-%m-%d %H:%M", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(datetime_str, fmt)
        except ValueError:
            continue
    raise ValueError(
        f"Time data '{datetime_str}' does not match any of the expected formats."
    )


def datetime_to_str(datetime_obj: datetime) -> str:
    """Converts a datetime into a standardized string representation

    Args:
        datetime_obj (datetime): a datetime object

    Returns:
        str: string representation of the datetime object
    """
    return datetime_obj.strftime(DATETIME_FORMAT)
