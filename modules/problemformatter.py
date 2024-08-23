import discord
from discord import app_commands

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

    if problem[4] == 'True\n': # the /n is for how the csv file is setup since it is the last row
        print("here")
        return discord.Embed(title = f"**{problem[2]}: {problem[0]}**", description = problem[1] + "\n*This is a premium problem*", color = assignColor(problem[3]))

    return discord.Embed(title = f"**{problem[2]}: {problem[0]}**", description = problem[1], color = assignColor(problem[3]))