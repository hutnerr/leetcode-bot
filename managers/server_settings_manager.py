from tools import database_helper as dbh

def getServerSettings(serverID):
    pass

def getChannelToSendTo(serverID):
    serverRow = dbh.getRow("servers", "serverID = ?", (serverID,))
    return parseServerSettings(serverRow)["channelID"]

def parseServerSettings(serverRow:tuple) -> dict:
    serverSettings = {
        "id" : serverRow[0],
        "channelID" : serverRow[1],
        "problems" : serverRow[2],
        "weeklyContests" : serverRow[3],
        "biweeklyContests" : serverRow[4],
        "timezone" : serverRow[5]
    }
    return serverSettings

