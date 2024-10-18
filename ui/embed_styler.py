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

# ############################################################
# Helper Functions
# ############################################################

# green = easy, yellow = medium, red = hard
def assignColor(difficulty: str) -> discord.Color:
    if difficulty == "Easy":
        return discord.Color.green()
    elif difficulty == "Medium":
        return discord.Color.yellow()
    elif difficulty == "Hard":
        return discord.Color.red()
    else:
        return discord.Color.blue()

def buildTimeString(timeDict:dict) -> str:
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

def styleProblem(problem:dict, problemSlug:str) -> str:
    # send a special message if the problem is premium
    
    em = discord.Embed(
        title = f"{problem['id']} - {problem['title']}",
        color = assignColor(problem["difficulty"]),
        url = pim.buildLinkFromSlug(problemSlug)
    )
    
    em.add_field(name = "Description", value = problem["description"], inline = False)
    
    for i in problem["examples"]:
        em.add_field(name = f"Example {i}", value = f"```{problem['examples'][i]}```", inline = False)

    return em

def styleProblemSimple(problem:dict, problemSlug:str) -> str:
    em = discord.Embed(
        title = f"{problem['id']} - {problem['title']}",
        color = assignColor(problem["difficulty"]),
        url = pim.buildLinkFromSlug(problemSlug)
    )
    
    em.add_field(name = "", value = "Error sending full problem description.\nEmbed size exceeded.", inline = False)
    
    return em

def styleContest(contestInfo:dict) -> discord.Embed:
    em = discord.Embed(
        title = "LeetCode Contests",
        color = discord.Color.blue(),
        url = "https://leetcode.com/contest/"
    )

    biweeklyTitle, biweeklyTime = contestInfo["biweekly"]
    biweeklyTimeDict = th.timedeltaToDict(biweeklyTime)
    em.add_field(name = biweeklyTitle, value = f"```{buildTimeString(biweeklyTimeDict)}```", inline = False)
    

    weeklyTitle, weeklyTime = contestInfo["weekly"]
    weeklyTimeDict = th.timedeltaToDict(weeklyTime)
    em.add_field(name = weeklyTitle, value = f"```{buildTimeString(weeklyTimeDict)}```", inline = False)
    

    return em
    
def styleActiveProblems(activeProblems:dict) -> discord.Embed:
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
    em = discord.Embed(
        title = title,
        description = description,
        color = color
    )
    
    return em