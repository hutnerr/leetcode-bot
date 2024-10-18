from tools import database_helper as dbh
from tools.consts import DatabaseTables as dt

def parseUserSettings(userRow:tuple):
    settings = {
        "userID": userRow[0],
        "leetcodeUsername": userRow[1],
        "serverID": userRow[2],
        "weeklyOpt": userRow[3],
        "biweeklyOpt": userRow[4],
        "problemOpt": userRow[5]
    }
    
    return settings

# TODO: Implement this function when I do the competition system
def addPoints(userID:int, points:int) -> None:
    pass