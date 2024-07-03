"""
Datetime utils to standardize conversion and manipulation of datetime objects.
All datetime related functions should be defined here to prevent assumptions about the format ]
of date-time objects and their string representations
"""

from datetime import datetime


def datetime_from_str(datetime_str: str) -> datetime:
    """Converts a string of a datetime into a Datetime object

    Args:
        datetime_str (str): a string representation of a datetime

    Raises:
        ValueError: If the string representation does not match a valid datetime format

    Returns:
        datetime: a datetime object
    """
    return datetime.fromisoformat(datetime_str)


def datetime_to_str(datetime_obj: datetime) -> str:
    """Converts a datetime into a standardized string representation

    Args:
        datetime_obj (datetime): a datetime object

    Returns:
        str: string representation of the datetime object
    """
    return datetime_obj.isoformat()
