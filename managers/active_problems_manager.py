from tools import database_helper as dbh
from tools.consts import DatabaseTables as dbt
from tools.consts import DatabaseFields as dbf

def updateActiveProblems(serverID, problemID, slug):
    if not dbh.contains(dbt.ACTIVE_PROBLEMS.value, "serverID = ?", (serverID,)):
        dbh.addRow(dbt.ACTIVE_PROBLEMS.value, dbf.ACTIVE_PROBLEMS.value, (serverID, "none", "none", "none"))
    
    dbh.updateRow(dbt.ACTIVE_PROBLEMS.value, f'p{problemID}', slug, f'serverID = {serverID}')
    dbh.printRows(dbt.ACTIVE_PROBLEMS.value)
    
def getActiveProblems(serverID):
    return dbh.getRow(dbt.ACTIVE_PROBLEMS.value, "serverID = ?", (serverID,))

def parseActiveProblems(row):
    activeProblems = {
        "p1": row[1],
        "p2": row[2],
        "p3": row[3]
    }
    
    return activeProblems

def getAndParseActiveProblems(serverID):
    return parseActiveProblems(getActiveProblems(serverID))