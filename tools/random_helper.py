"""
Simple helper functions for random number generation or random selection

Functions:
    - getRandom(lst: list) -> any
    - getRandomRange(start: int = 1, end: int = 5) -> int
"""
import random

def getRandom(lst: list) -> any:
    """
    Gets a random value from the passed in list 
    Args:
        lst (list): The list to select from
    Returns:
        any: A random value from the list provided
    """
    return random.choice(lst)

def getRandomRange(start: int = 1, end: int = 5) -> int:
    """
    Get a random number within the provided range
    Args:
        start (int, optional): The start of the range. Defaults to 1.
        end (int, optional): The end of the range. Defaults to 5.
    Returns:
        int: The random number within the range
    """
    return random.randint(start, end)