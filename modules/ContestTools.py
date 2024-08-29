import json
from datetime import datetime, timezone

filepath = "data/contests.json"

# comment this and make it less ugly 
def increaseContestNum(contest):
    with open(filepath, 'r+') as f:
        data = json.load(f)
        data[contest]["number"] += 1
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

# comment this and give better variable names 
def getContestTime(contest):

    dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

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

    current_time = datetime.now().astimezone(timezone.utc)
    current_day = current_time.strftime("%A")
    current_time = current_time.strftime("%H:%M:%S")

    daysLeft = (dayIndex - dow.index(current_day)) % 7

    hoursLeft = (datetime.strptime(contests['time'], "%H:%M") - datetime.strptime(current_time, "%H:%M:%S")) # % datetime.timedelta(hours=24)

    if hoursLeft.days < 0:
        daysLeft -= 1
        hoursLeft = hoursLeft + datetime.timedelta(hours=24)

    return [daysLeft, hoursLeft]

out = getContestTime("biweekly")
print(f"{out[0]} days and {out[1]} hours left") 

