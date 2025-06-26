import json
import requests
import os

from utils import csv_helper as csvh

PROBLEMS_URL = "https://www.leetcode.com/problems/"

def titleToSlug(title: str) -> str:
    # i.e. Two Sum -> two-sum
    return title.replace(" ", "-").lower()

def slugToTitle(slug: str) -> str:
    # i.e. two-sum -> Two Sum
    return " ".join([word.capitalize() for word in slug.split("-")])

# creates a link to a problem using its slug
def slugToURL(slug: str) -> str:
    return f"{PROBLEMS_URL}{slug}"

# updates the problem set by fetching the latest problems from LeetCode
# and saving them to a CSV file
def updateProblemSet() -> bool:
    problemList = json.loads(requests.get("https://leetcode.com/api/problems/all/").content)
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
    
    path = os.path.join("data", "problems.csv")
    csvh.writeLinesToCSV(path, problems, True)