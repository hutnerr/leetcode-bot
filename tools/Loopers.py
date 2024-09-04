# check every 10 seconds for when my minutes are at 00 then use the hour to find the related text file
# this related text file will contain all of the server ids whos assigned to this time.
# read the file into a list
# loop through the list while calling a function like applyDaily(serverID) for each server. 


from modulesSmile import ProblemsHandler as ph
from modulesSmile import SettingHandler as sh

def applyDaily(sid):
    fp = "data/serverdata/sid.json"
    data = sh.getServerFile(sid)
    channelid = data['dailies']['channel']

    problemset = None

    premium = data['dailies']['premium']
    if premium == "true":
        problemset = "paid_problems.csv"
    elif premium == "false":
        problemset = "free_problems.csv"
    else:
        problemset = "all_problems.csv"

    problem = ph.getProblem(problemset, data['dailies']['difficulty'])

    return [sid, channelid, problem]




