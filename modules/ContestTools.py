import datetime
import json

def increaseContestNum(contestfile):
    with open(contestfile, 'r+') as f:
        num = int(f.readline()) + 1
        f.seek(0)
        f.write(str(num))

def getContestTime(contest):

    dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    filepath = "data/contests.json"
    contests = None

    with open(filepath, 'r') as f:
        contests = json.load(f)

        if contest == "weekly":
            contests = contests["weekly"]
        elif contest == "biweekly":
            contests = contests["biweekly"]
        else:
            return "Invalid"
        
    dayIndex = dow.index(contests["day"])

    current_time = datetime.datetime.now()
    current_day = current_time.strftime("%A")
    current_time = current_time.strftime("%H:%M:%S")

    daysLeft = (dayIndex - dow.index(current_day)) % 7

    hoursLeft = (datetime.datetime.strptime(contests['time'], "%H:%M") - datetime.datetime.strptime(current_time, "%H:%M:%S")) % datetime.timedelta(hours=24)

    return [daysLeft, hoursLeft]

out = getContestTime("biweekly")
print(f"{out[0]} days and {out[1]} hours left") # this is still wrong, bi weekly days are off. can i monkey it and do - 1?