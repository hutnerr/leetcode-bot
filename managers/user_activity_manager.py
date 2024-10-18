"""
This file contains functions that interact with the user activity.
Performs queries and other checks. 

Functions:
    getRecentProblemsSolved(username: str, amount: int = 5) -> list
    checkIfRecentlySolved(userID: int, problemSlug: str) -> bool
"""
from tools import query_helper as qh
from tools.consts import Query as q

from managers import user_activity_manager as uam

def getRecentProblemsSolved(username: str, amount: int = 5) -> list:
    """ 
    Get the most recent problems solved by a user
    
    Args:
        username (str): The LeetCode username of the user
        amount (int): The amount of problems to get. If not specified, it will default to 5
    Returns:
        list: A list of the `amount` recent problems solved by the user    
    """
    result = qh.performQuery(q.RECENT_SUBMISSIONS.value, {"username": username, "limit": amount})
    result = result["data"]["recentAcSubmissionList"] # trim the query result
    for i in range(len(result)):
        result[i] = result[i]["titleSlug"] # only keep the slug
    return result

def checkIfRecentlySolved(userID: int, problemSlug: str) -> bool:
    """
    Performs a query to check if a user has solved a problem recently
    Args:
        userID (int): The discord ID of the user
        problemSlug (str): The slug of the problem to check 
    Returns:
        bool: True if the user has solved the problem recently, False otherwise
    """
    username = uam.getUsernameFromID(userID)
    problems = getRecentProblemsSolved(username)
    return problemSlug in problems
    
    