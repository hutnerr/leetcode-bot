"""
Handles building the problem sets from the leetcode api

Functions:
    - buildList() -> list
    - buildCSV(problems: list) -> None
    - scrapeAndBuild() -> None
"""
import requests
import csv
import json
import os

from tools.consts import URLS as urls
from tools.consts import Problemset as ps

def buildList() -> list:
    """
    This method will scrape the leetcode api page and build a list of all problems.
    Returns:
        list: The tuple of scraped problems in the form of a tuple where
            - ('titleSlug', 'difficulty', paid)
            - ('two-sum', 'Easy', False)
    """
    problemList = json.loads(requests.get(urls.LEETCODE_PROBLEMS.value).content)
    problems = []
    for child in problemList["stat_status_pairs"]:
        titleSlug = child["stat"]["question__title_slug"]
        difficulty = child["difficulty"]["level"]
        
        if difficulty == 1:
            difficulty = "Easy"
        elif difficulty == 2:
            difficulty = "Medium"
        elif difficulty == 3:
            difficulty = "Hard"
        else:
            difficulty = "Unknown"
        
        paid = child["paid_only"]
        problems.append((titleSlug, difficulty, paid))
    return problems

# This method will use the list of problems and build three separate CSV files with the data
def buildCSV(problems: list) -> None:
    """
    Uses the list of scraped problems to build three separate CSV files with the data.
    Args:
        problems (list): The scraped problems list
    """
    path = os.path.join("data", "problem_sets")
    
    # open and write to the csv files
    files = {
        ps.FREE.value: [],
        ps.PAID.value: [],
        ps.BOTH.value: []
    }

    for problem in problems:
        files[ps.BOTH.value].append(problem)
        if problem[2]:  # check if the problem is paid
            files[ps.PAID.value].append(problem)
        else:
            files[ps.FREE.value].append(problem)

    for filename, rows in files.items():
        with open(os.path.join(path, filename), mode = 'w', newline = '', encoding = "utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(("Slug", "Difficulty", "Paid"))
            writer.writerows(rows)

def scrapeAndBuild() -> None:
    """
    Gets the list of problems and then builds the CSV files.
    """
    problems = buildList()
    buildCSV(problems)