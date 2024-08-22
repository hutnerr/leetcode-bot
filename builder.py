import requests
import csv
import json
import os

# this scraper should only handle scraping the problems. not random selection etc. 

# this is an api endpoint i may be able to check if people have completed a problem
# https://leetcode.com/graphql

scrapeURL = "https://leetcode.com/api/problems/all/"
buildURL = "https://leetcode.com/problems/"

# This method will scrape the leetcode website and build a list of all problems.
def buildList():
    problemList = json.loads(requests.get(scrapeURL).content)
    problems = []
    for child in problemList["stat_status_pairs"]:
        title = child["stat"]["question__title"]                        # proper name
        titleSlug = buildURL + child["stat"]["question__title_slug"]    # for building URL
        frontend_question_id = child["stat"]["frontend_question_id"]    # the problem number 
        difficulty = child["difficulty"]["level"]                       # difficulty level. 1 = easy, 2 = medium, 3 = hard
        paid = child["paid_only"]                                       # true if it's a premium question
        problems.append([title, titleSlug, frontend_question_id, difficulty, paid])
    return problems

# This method will use the list of problems and build three separate CSV files with the data
def buildCSV(problems):
    with open('data/all_problems.csv', mode='w', newline='', encoding="utf-8") as all_file:
        with open('data/paid_problems.csv', mode='w', newline='', encoding="utf-8") as paid_file:
            with open('data/free_problems.csv', mode='w', newline='', encoding="utf-8") as free_file:
                all_writer = csv.writer(all_file)
                paid_writer = csv.writer(paid_file)
                free_writer = csv.writer(free_file)
                all_writer.writerow(("Title", "URL", "ID", "Difficulty", "Paid"))
                paid_writer.writerow(("Title", "URL", "ID", "Difficulty", "Paid"))
                free_writer.writerow(("Title", "URL", "ID", "Difficulty", "Paid"))
                for problem in problems:
                    all_writer.writerow(problem)
                    if problem[4]:  # check if the problem is paid
                        paid_writer.writerow(problem)
                    else:
                        free_writer.writerow(problem)

# This method will scrape the leetcode website and update a CSV file with the data
# This is the only method i want people to be able to use from this class 
def scrapeAndBuild():
    problems = buildList()
    buildCSV(problems)


# Create 3 separate files. 
# 1. all problems, only free, only premium
# rn it is only the one
    
scrapeAndBuild()