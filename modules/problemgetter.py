import random
import os
import csv

PATH = 'data/'

def getProblem(file:str, dif:str):
    with open(os.path.join(PATH, file), "r") as f:
        data = f.readlines()

    # special case for any difficulty
    if dif == "0":
        return random.choice(data).split(",")
    
    # filter our problems into the difficulty then make the random choice. 
    filtered = [problem.split(",") for problem in data if problem.split(",")[3] == dif]
    problem = random.choice(filtered)
    return problem