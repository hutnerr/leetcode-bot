"""
Manager for handling the settings of problems for a server

Functions:
    - getProblemCount(serverID: int) -> int
    - increaseProblemCount(serverID: int) -> bool
    - decreaseProblemCount(serverID: int) -> bool
    - addProblem(serverID: int, problemID: int, dow: str, hour: int, difficulty: str, premium: str) -> bool
    - removeProblem(serverID: int, problemID: int) -> bool
    - updateProblem(serverID: int, problemID: int, column: str, value: any) -> bool
    - getProblems(serverID: int) -> tuple
    - getProblem(serverID: int, problemID: int) -> tuple
    - parseProblemSettings(problemRow: tuple) -> dict
    - getAndParseProblem(serverID: int, problemID: int) -> dict
    - buildLinkFromSlug(slug: str) -> str
    - getProblemInfo(slug: str) -> dict
    - getExamples(problemDescription: str) -> dict
"""
from bs4 import BeautifulSoup

from managers import server_settings_manager as ssm

from tools import database_helper as dbh
from tools import query_helper as qh
from tools.consts import Boundaries as bounds
from tools.consts import DatabaseFields as dbf
from tools.consts import DatabaseTables as dbt
from tools.consts import Query as q

# ############################################################
# Problem Counters
# ############################################################

def getProblemCount(serverID: int) -> int:
    """
    Get the number of problems a server has set up
    Args:
        serverID (int): The Discord Server ID 
    Returns:
        int: The number of problems the server has set up
    """
    serverRow = dbh.getRow(dbt.SERVERS.value, "serverID = ?", (serverID,))
    settings = ssm.parseServerSettings(serverRow)
    return settings['problems']

def increaseProblemCount(serverID: int) -> bool:
    """
    Increase the number of problems a server has set up
    Args:
        serverID (int): The Discord Server ID
    Returns:
        bool: True if the problem count was successfully increased, False otherwise
    """
    problemCount = getProblemCount(serverID)
    
    if problemCount >= bounds.MAX_PROBLEMS.value:
        print("Error: Problem count is already at maximum")
        return False
    else:
        dbh.updateRow("servers", "problems", problemCount + 1, f"serverID = {serverID}")
        return True
    
def decreaseProblemCount(serverID: int) -> bool:
    """
    Decrease the number of problems a server has set up
    Args:
        serverID (int): The Discord Server ID
    Returns:
        bool: True if the problem count was successfully decreased, False otherwise
    """
    problemCount = getProblemCount(serverID)
    
    if problemCount <= bounds.MIN_PROBLEMS.value:
        print("Error: Problem count is already at minimum")
        return False
    else:
        dbh.updateRow(dbt.SERVERS.value, "problems", problemCount - 1, f"serverID = {serverID}")
        return True
        
# ############################################################
# Adding, Removing, & Updating Problems
# ############################################################

def addProblem(serverID: int, problemID: int, dow: str, hour: int, difficulty: str, premium: str) -> bool:
    """
    Try and add a problem to our problems database
    Args:
        serverID (int): The Discord ID of the server we're adding the problem to
        problemID (int): The problem number
        dow (str): The days of the week the problem is available e.g. "Monday,Wednesday,Friday"
        hour (int): The hour the problem is available. e.g. 0 - 23
        difficulty (str): The difficulty string of the problem. e.g. "Easy,Medium"
        premium (str): The dataset we want to use. e.g. "Free" or "Paid" or "Both"
    Returns:
        bool: True if the problem was successfully added, False otherwise
    """
    # if we dont have and we we're not at max, then we can add
    if not dbh.contains(dbt.PROBLEMS.value, "serverID = ? and problemNum = ?") and increaseProblemCount(serverID):
        dbh.addRow(dbt.PROBLEMS.value, (dbf.PROBLEMS.value), (serverID, problemID, dow, hour, difficulty, premium))
        return True
    return False

def removeProblem(serverID: int, problemID: int) -> bool:
    """
    Remove a problem from our problems database
    Args:
        serverID (int): The Discord ID of the server we're removing the problem from
        problemID (int): The Problem ID we're removing
    Returns:
        bool: True if the problem was successfully removed, False otherwise
    """
    # if we have the row and not at min, then remove
    if dbh.contains(dbt.PROBLEMS.value, "serverID = ? and problemNum = ?", (serverID, problemID)) and decreaseProblemCount(serverID):
        dbh.removeRow(dbt.PROBLEMS.value, "serverID = ? AND problemNum = ?", (serverID, problemID))
        return True
    return False

def updateProblem(serverID: int, problemID: int, column: str, value: any) -> bool:
    """
    Update a problem in our problems database
    Args:
        serverID (int): The Discord ID of the server we're updating the problem for
        problemID (int): The Problem ID we're updating
        column (str): The column of the problem we want to change
        value (any): What we want to change it to 
    Returns:
        bool: True if the problem was successfully updated, False otherwise
    """
    # if it exists we can update
    if dbh.contains(dbt.PROBLEMS.value, "serverID = ? and problemNum = ?", (serverID, problemID)):
        dbh.updateRow(dbt.PROBLEMS.value, column, value, f"serverID = {serverID} AND problemNum = {problemID}")
        return True
    return False

# ############################################################
# Getters
# ############################################################

def getProblems(serverID: int) -> tuple:
    """
    Get all the problems for a server
    Args:
        serverID (int): The Discord ID of the server we're getting the problems for
    Returns:
        tuple: The rows of the problems
    """
    return dbh.getRowsWhere(dbt.PROBLEMS.value, "serverID = ?", (serverID,))

def getProblem(serverID: int, problemID: int) -> tuple:
    """
    Get a problem from our problems database
    Args:
        serverID (int): The Discord ID of the server we're getting the problem from
        problemID (int): The Problem ID we're getting
    Returns:
        tuple: The Database row 
    """
    return dbh.getRow(dbt.PROBLEMS.value, "serverID = ? AND problemNum = ?", (serverID, problemID))

def parseProblemSettings(problemRow: tuple) -> dict:
    """
    Parse the settings of a problem into a dictionary
    Args:
        problemRow (tuple): The database row of the problem
    Returns:
        dict: The settings of the problem. Contains:
            - serverID (int): The Discord ID of the server
            - problemNum (int): The Problem ID
            - dow (str): The dow string the problem is available e.g. "Monday,Wednesday,Friday"
            - hour (int): The hour the problem is available e.g. 0 - 23
            - difficulty (str): The difficulty string of the problem e.g. "Easy,Medium"
            - premium (str): The dataset we want to use. e.g. "Free" or "Paid" or "Both"
    """
    settings = {
        "serverID" : problemRow[0],
        "problemNum" : problemRow[1],
        "dow" : problemRow[2],
        "hour" : problemRow[3],
        "difficulty" : problemRow[4],
        "premium" : problemRow[5]
    }
    return settings

def getAndParseProblem(serverID: int, problemID: int) -> dict:
    """
    Gets and parses the settings of a problem into a dict 
    Args:
        serverID (int): The Discord ID of the server we're getting the problem from
        problemID (int): The Problem ID we're getting
    Returns:
        dict: The settings of the problem. Contains:
            - serverID (int): The Discord ID of the server
            - problemNum (int): The Problem ID
            - dow (str): The dow string the problem is available e.g. "Monday,Wednesday,Friday"
            - hour (int): The hour the problem is available e.g. 0 - 23
            - difficulty (str): The difficulty string of the problem e.g. "Easy,Medium"
            - premium (str): The dataset we want to use. e.g. "Free" or "Paid" or "Both"
    """
    problem = getProblem(serverID, problemID)
    return parseProblemSettings(problem)


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
    """
    Separates the examples from the description. 
    Args:
        problemDescription (str): The problem description
    Returns:
        dict: A dictionary of examples. Contains:
            - key (int): The example number. e.g 1
            - value (str): The example. e.g "Example 1 Content"
    """
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
