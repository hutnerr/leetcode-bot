"""
This is a simple helper utility for various file operations

Functions:
    fileToList(filepath: str) -> list
"""

def fileToList(filepath: str) -> list:
    """
    Opens a file and converts its lines into a list
    Args:
        filepath (str): The path to the file
    Returns:
        list: The lines of the file at filepath
    """
    with open(filepath, "r") as file:
        return file.read().splitlines()
