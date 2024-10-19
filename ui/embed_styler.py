"""
UI Styler for Discord Embeds

Functions:
    assignColor(difficulty: str) -> discord.Color
    buildTimeString(timeDict:dict) -> str
    styleProblem(problem:dict, problemSlug:str) -> str
    styleProblemSimple(problem:dict, problemSlug:str) -> str
    styleContest(contestInfo:dict) -> discord.Embed
    styleActiveProblems(activeProblems:dict) -> discord.Embed
    styleSimpleEmbed(title:str, description:str, color:discord.Color) -> discord.Embed
"""
import discord

from managers import problem_info_manager as pim
from managers import daily_problem_manager as dpm

from tools import time_helper as th
from tools.consts import URLS as urls

# ############################################################
# Helper Functions
# ############################################################

def assignColor(difficulty: str) -> discord.Color:
    """
    Gets a color based on the difficulty of the problem.\n
    Easy = Green, Medium = Yellow, Hard = Red, Other = Blue
    Args:
        difficulty (str): The difficulty as a string. e.g. "Easy"
    Returns:
        discord.Color: The appropriate color 
    """
    if difficulty == "Easy":
        return discord.Color.green()
    elif difficulty == "Medium":
        return discord.Color.yellow()
    elif difficulty == "Hard":
        return discord.Color.red()
    else:
        return discord.Color.blue()

def buildTimeString(timeDict: dict) -> str:
    """
    Builds a string from a dictionary of time values.\n
    Used for polish. e.g. accounts for pluralization and 0 values
    Args:
        timeDict (dict): The dictionary of time values. e.g. {"days": 1, "hours": 2, "minutes": 3}. Built from time_helper.timedeltaToDict
    Returns:
        str: The build string. e.g. "1 day, 2 hours, and 3 minutes away"
    """
    timeString = ""
    if timeDict["days"] > 0:
        if timeDict["days"] == 1:
            timeString += f"{timeDict['days']} day, "
        else:
            timeString += f"{timeDict['days']} days, "
        
    if timeDict["hours"] > 0:
        if timeDict["hours"] == 1:
            timeString += f"{timeDict['hours']} hour, "
        else:
            timeString += f"{timeDict['hours']} hours, "
    
    if timeDict["minutes"] > 0:
        if timeDict["minutes"] == 1:
            timeString += f"and {timeDict['minutes']} minute away"
        else:
            timeString += f"and {timeDict['minutes']} minutes away"

    return timeString

# ############################################################
# Embed Styling Functions
# ############################################################

def styleProblem(problemInfo: dict) -> discord.Embed:
    """
    Styles a problem into an embed for Discord. Includes the problem description and examples.
    Args:
        problemInfo (dict): The problemInfo dictionary from problem_info_manager.getProblemInfo()
    Returns:
        discord.Embed: The styled embed
    """
    em = discord.Embed(
        title = f"{problemInfo['id']} - {problemInfo['title']}",
        color = assignColor(problemInfo["difficulty"]),
        url = pim.buildLinkFromSlug(problemInfo["slug"])
    )
    em.add_field(name = "Description", value = problemInfo["description"], inline = False)

    for i in problemInfo["examples"]:
        em.add_field(name = f"Example {i}", value = f"```{problemInfo['examples'][i]}```", inline = False)

    return em

def styleProblemSimple(problemInfo: dict) -> discord.Embed:
    """
    Returns an embed with a simple message that says a problem occured when trying to send the full problem description.\nProvides the title and a link to the problem.
    Args:
        problemInfo (dict): The problemInfo dictionary from problem_info_manager.getProblemInfo()
    Returns:
        discord.Embed: The simply styled embed
    """
    em = discord.Embed(
        title = f"{problemInfo['id']} - {problemInfo['title']}",
        color = assignColor(problemInfo["difficulty"]),
        url = pim.buildLinkFromSlug(problemInfo["slug"])
    )
    em.add_field(name = "", value = "Error sending full problem description. Please visit link.\nEmbed size exceeded.", inline = False)
    
    return em

def styleContest(contestInfo: dict) -> discord.Embed:
    """
    Styles the contest times into an embed for Discord.
    Args:
        contestInfo (dict): The contest info dictionary from contest_manager.getAndParseContestsInfo()
    Returns:
        discord.Embed: The styled mebed of the contest times
    """
    em = discord.Embed(
        title = "LeetCode Contests",
        color = discord.Color.blue(),
        url = urls.LEETCODE_CONTESTS.value
    )

    biweeklyTitle, biweeklyTime = contestInfo["biweekly"]
    biweeklyTimeDict = th.timedeltaToDict(biweeklyTime)
    em.add_field(name = biweeklyTitle, value = f"```{buildTimeString(biweeklyTimeDict)}```", inline = False)

    weeklyTitle, weeklyTime = contestInfo["weekly"]
    weeklyTimeDict = th.timedeltaToDict(weeklyTime)
    em.add_field(name = weeklyTitle, value = f"```{buildTimeString(weeklyTimeDict)}```", inline = False)

    return em
    
def styleActiveProblems(activeProblems: dict) -> discord.Embed:
    """
    Styles the active problems into an embed for Discord. Includes the official daily problem. 
    Args:
        activeProblems (dict): The dict of the active problems from active_problems_manager.getAndParseActiveProblems()
    Returns:
        discord.Embed: The styles embed for the active problems within the server
    """
    em = discord.Embed(
        title = "Active Problems",
        color = discord.Color.purple()
    )
    
    officialDaily = dpm.getOfficialDailyProblemInfo()
    em.add_field(name = "Official Daily", value = f'[{officialDaily["title"]}]({officialDaily["url"]})', inline = False)
    
    for problem in activeProblems:
        problemInfo = pim.getProblemInfo(activeProblems[problem])
        em.add_field(name = f'Problem {problem.replace("p", "")}', value = f'[{problemInfo["title"]}]({problemInfo["url"]})', inline = False)
    
    return em

def styleSimpleEmbed(title:str, description:str, color:discord.Color) -> discord.Embed:
    """
    Simple template embed for Discord. Used for simple messages.
    Args:
        title (str): _description_
        description (str): _description_
        color (discord.Color): _description_
    Returns:
        discord.Embed: The simple embed 
    """
    em = discord.Embed(
        title = title,
        description = description,
        color = color
    )
    return em