import requests
import csv
import json
import os

scrapeURL = "https://leetcode.com/api/problems/all/"

# This method will scrape the leetcode api page and build a list of all problems.
def buildList():
    problemList = json.loads(requests.get(scrapeURL).content)
    problems = []
    for child in problemList["stat_status_pairs"]:                   # proper name
        titleSlug = child["stat"]["question__title_slug"]    # for building URL
        difficulty = child["difficulty"]["level"]                       # difficulty level. 1 = easy, 2 = medium, 3 = hard
        paid = child["paid_only"]                                       # true if it's a premium question
        problems.append([titleSlug, difficulty, paid])
    return problems

# This method will use the list of problems and build three separate CSV files with the data
def buildCSV(problems):
    path = os.path.join("data", "problem_sets")
    
    with open(os.path.join(path, "all.csv"), mode='w', newline='', encoding="utf-8") as all_file:
        with open(os.path.join(path, "paid.csv"), mode='w', newline='', encoding="utf-8") as paid_file:
            with open(os.path.join(path, "free.csv"), mode='w', newline='', encoding="utf-8") as free_file:
                all_writer = csv.writer(all_file)
                paid_writer = csv.writer(paid_file)
                free_writer = csv.writer(free_file)
                all_writer.writerow(("Slug", "Difficulty", "Paid"))
                paid_writer.writerow(("Slug", "Difficulty", "Paid"))
                free_writer.writerow(("Slug", "Difficulty", "Paid"))
                for problem in problems:
                    all_writer.writerow(problem)
                    if problem[2]:  # check if the problem is paid
                        paid_writer.writerow(problem)
                    else:
                        free_writer.writerow(problem)

# This method will scrape the leetcode website and update a CSV file with the data
# This is the only method i want people to be able to use from this class 
def scrapeAndBuild():
    problems = buildList()
    buildCSV(problems)
