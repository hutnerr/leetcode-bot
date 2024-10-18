"""
Manager for things related to the official daily LeetCode problem.

Functions:
    - getOfficialDailyProblemSlug() -> str: 
    - getOfficialDailyProblemInfo() -> dict:
    - getTimeLeftUntilOfficialDailyReset() -> str:
"""
from tools import query_helper as qh
from tools import time_helper as th
from tools.consts import Query as q
from tools.consts import Times as t

from managers import problem_info_manager as pim

from datetime import datetime

def getOfficialDailyProblemSlug() -> str:
    """
    Performs a query to retrieve the daily probelem slug
    Returns:
        str: The slug of the daily problem
    """
    out = qh.performQuery(q.DAILY_PROBLEM.value, {})
    return out['data']['challenge']['question']['titleSlug']

def getOfficialDailyProblemInfo() -> dict:
    """
    Gets a dict of the problemInfo of the daily problem. From problem_info_manager.getProblemInfo
    Returns:
        dict: The dict of the problemInfo of the daily problem. From problem_info_manager.getProblemInfo
    """
    return pim.getProblemInfo(getOfficialDailyProblemSlug())

def getTimeLeftUntilOfficialDailyReset() -> str:
    """
    Calculates the time left until the official daily problem resets
    Returns:
        str: The time left until reset. Format: hours:mins:secs
    """
    now = th.getCurrentTime()
    resetTime = datetime.strptime(t.OFFICIAL_DAILY_RESET.value, "%H:%M").replace(year = now.year, month = now.month, day = now.day)
    timeAway = th.distanceAway(resetTime)
    return str(timeAway).split(".")[0] # gets only hours:mins:secs