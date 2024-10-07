import discord
from discord import app_commands

import random
import os
import csv


##################################################################################### Retrieval 

def getProblem(file:str, dif:str) -> list:
    with open(os.path.join("data", "problems", file), "r") as f:
        data = f.readlines()
    
    # list will be [1, 2, 3] for easy, medium, hard
    listDif = dif.split(",")

    # if there is only or two difficulties, we need to filter the problems to only those difficulties
    if len(listDif) == 1:
        filtered = [problem.split(",") for problem in data if problem.split(",")[3] == listDif[0]]
    elif len(listDif) == 2:
        filtered = [problem.split(",") for problem in data if problem.split(",")[3] == listDif[0] or problem.split(",")[3] == listDif[1]]
    else:
        # if we have 3 difficulties, we can just return a random problem from the list, no filtering needed
        return random.choice(data).split(",")

    # now that we've filtered, we can make our random choice 
    problem = random.choice(filtered)
    return problem

##################################################################################### Visuals 

# green = easy, yellow = medium, red = hard
def assignColor(difficulty: str) -> discord.Color:
    if difficulty == "1":
        return discord.Color.green()
    elif difficulty == "2":
        return discord.Color.yellow()
    elif difficulty == "3":
        return discord.Color.red()
    else:
        return discord.Color.blue()

def prettifyProblem(problem: list) -> str:
    # send a special message if the problem is premium
    if problem[4] == 'True\n': # the /n is for how the csv file is setup since it is the last row
        return discord.Embed(title = f"**{problem[2]}: {problem[0]}**", description = problem[1] + "\n*This is a premium problem*", color = assignColor(problem[3]))

    return discord.Embed(title = f"**{problem[2]}: {problem[0]}**", description = problem[1], color = assignColor(problem[3]))

