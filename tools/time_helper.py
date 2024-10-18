""" 
Helper for working with some time functions

Functions:
    - timeDifference(then: datetime, now: datetime) -> datetime
    - distanceAway(then: datetime) -> datetime
    - fromTimestamp(timestamp: int) -> datetime
    - getCurrentTime() -> datetime
    - timedeltaToDict(delta: datetime) -> dict
"""

from datetime import datetime

def timeDifference(then: datetime, now: datetime) -> datetime:
    """
    Calculates the difference between two datetime objects
    Args:
        then (datetime): When the event will happen
        now (datetime): What time it is now
    Returns:
        datetime: The difference between the two times
    """
    return then - now

def distanceAway(then: datetime) -> datetime:
    """
    Calculates the difference between now and a given time
    Args:
        then (datetime): The time we want to calculate the difference from
    Returns:
        datetime: The difference between now and the given time
    """
    return timeDifference(then, getCurrentTime())

def fromTimestamp(timestamp: int) -> datetime:
    """
    Converts a POSIX timestamp to a datetime object
    Args:
        timestamp (int): The POSIX timestamp
    Returns:
        datetime: The datetime object we converted to
    """
    return datetime.fromtimestamp(timestamp)

def getCurrentTime() -> datetime:
    """
    Gets the current time
    Returns:
        datetime: The current time as a datetime object
    """
    return datetime.now()

def timedeltaToDict(delta: datetime) -> dict:
    """
    Converts a timedelta object to a dictionary
    Args:
        delta (datetime): The timedelta object
    Returns:
        dict: The dictionary representation of the timedelta. Contains:
            - days (int): The number of days
            - hours (int): The number of hours
            - minutes (int): The number of minutes
            - seconds (int): The number of seconds
    """
    timeDict = {
        "days" : delta.days,
        "hours" : delta.seconds // 3600,
        "minutes" : (delta.seconds // 60) % 60,
        "seconds" : delta.seconds % 60
    }
    return timeDict