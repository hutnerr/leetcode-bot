

from tools import query_helper as qh
from tools.consts import Query as q

from bs4 import BeautifulSoup


def buildLinkFromSlug(slug: str) -> str:
    """
    Build a leetcode problem link from a problem slug
    Args:
        slug (str): The problem slug
    Returns:
        str: The URL of the problem
    """
    return f"https://leetcode.com/problems/{slug}/"


def getProblemInfo(slug: str) -> dict:
    """
    Perform a query to get the problem info from leetcode then builds info dict
    Args:
        slug (str): The problem slug
    Returns:
        dict: The problemInfo dict. Contains:
            - id (int): The problem ID. e.g 1
            - title (str): The problem title. e.g "Two Sum"
            - difficulty (str): The problem difficulty. e.g "Easy"
            - description (str): The problem description / instruction. 
            - examples (dict): The problem examples. e.g {1: "Example 1", 2: "Example 2"}
            - slug (str): The problem slug. e.g "two-sum"
            - url (str): The problem URL. e.g "https://leetcode.com/problems/two-sum/"
            - isPaid (bool): True if the problem is a premium problem, False otherwise
    """
    problemInfo = qh.performQuery(q.QUESTION_INFO.value, {"titleSlug" : slug})
    problemInfo = problemInfo["data"]["question"]
    
    info = {
        "id" : problemInfo["questionFrontendId"],
        "title" : problemInfo["title"],
        "difficulty" : problemInfo["difficulty"],
        "description" : "",
        "examples" : {},
        "slug" : slug,
        "url" : buildLinkFromSlug(slug),
        "isPaid" : problemInfo["isPaidOnly"]
    }
    
    isPaid = problemInfo["isPaidOnly"]
        
    # Since we can't get the content of a premium problem, we set an notif for the user
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

