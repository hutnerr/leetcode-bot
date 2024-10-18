import json

from tools import query_helper as qh
from tools.consts import Query as q

from bs4 import BeautifulSoup

# --------------------------------- # 
# Builder Functions
# --------------------------------- #

def buildLinkFromSlug(slug: str) -> str:
    return f"https://leetcode.com/problems/{slug}/"

# --------------------------------- # 
# Problem info Functions
# --------------------------------- #

def getProblemInfo(slug: str) -> dict:
    
    problemInfo = qh.performQuery(q.QUESTION_INFO.value, {"titleSlug" : slug})
    problemInfo = problemInfo["data"]["question"]
    
    info = {
        "id" : problemInfo["questionFrontendId"],
        "title" : problemInfo["title"],
        "difficulty" : problemInfo["difficulty"],
        "description" : "",
        "examples" : {},
        "url" : buildLinkFromSlug(slug)
    }
    
    isPaid = problemInfo["isPaidOnly"]
        
    if not isPaid:
        soup = BeautifulSoup(problemInfo["content"], "html.parser")
        tempContent = soup.get_text() # get the text from the html content
        
        tempContent = tempContent[:tempContent.find("Constraints:")] # remove constraints section
        
        info["description"] = tempContent[:tempContent.find("Example 1:")].strip() # get the description
        info["examples"] = getExamples(tempContent)
    else:
        info["description"] = "This is a premium problem. Please visit the link for more information."
        info["examples"] = {}
    
    return info

def getExamples(problemDescription: str) -> dict:
    examples = {}
    
    i = 1
    while True:
        # get our example range
        start = problemDescription.find(f"Example {i}:")
        end = problemDescription.find(f"Example {i + 1}:")
        
        # prevent infinite loop & add limit
        if i == 5:
            break
        
        # break if we couldn't find a start 
        if start == -1:
            break
        # if we found a start, but not an end, we know we're at the last example
        elif end == -1:
            examples[i] = problemDescription[start:].strip()
            examples[i] = examples[i].replace(f"Example {i}:", "").strip()
            break
        else:
            examples[i] = problemDescription[start:end].strip()
            examples[i] = examples[i].replace(f"Example {i}:", "").strip()
        i += 1

    return examples

# --------------------------------- # 
# Print Functions
# --------------------------------- #

def printjson(jsonString: str) -> None:
    print(json.dumps(jsonString, indent=4))
    
def printProblemInfo(problemInfo: dict) -> None:
    print(f"ID: {problemInfo['id']}")
    print(f"Title: {problemInfo['title']}")
    print(f"Difficulty: {problemInfo['difficulty']}")
    print(f"Description: {problemInfo['description']}")
    print("Examples:")
    for i in problemInfo["examples"]:
        print(f"{problemInfo['examples'][i]}")
    

