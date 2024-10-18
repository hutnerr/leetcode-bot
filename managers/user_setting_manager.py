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