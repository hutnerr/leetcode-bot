import json
import os
from datetime import datetime, timezone

import json_reader as jr

# This file contains helper functions that track contests. 

filepath = os.path.join(jr.filepath(), "data", "contests.json")

# This function exists due to the fact that I'm keeping track of the number of contests locally
# It should be called whenever a contest is created
# The contest parameter should be either "weekly" or "biweekly"
def increaseContestNum(contest: str) -> None:
        
    with open(filepath, 'r+') as f: 
        data = json.load(f)
        data[contest]["number"] += 1
        f.seek(0) # Move the file pointer to the beginning of the file
        json.dump(data, f, indent = 4) # Write the data to the file
        f.truncate() # Truncate the file to the current file position

# Use the current datetime to determine how many days and hours are left until the contest
# The contest parameter should be either "weekly" or "biweekly"
# Returns a list of the form [daysLeft, hoursLeft]
def getContestTime(contest: str) -> list:

    dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    contestInfo = None

    with open(filepath, 'r') as f:
        contestInfo = json.load(f)[contest]

    dayIndex = dow.index(contestInfo["day"]) # The index of the day of the week the contest is on

    current_time = datetime.now().astimezone(timezone.utc) # Use UTC as a standardization
    current_day = current_time.strftime("%A")
    current_time = current_time.strftime("%H:%M:%S")

    daysLeft = (dayIndex - dow.index(current_day)) % 7 # % 7 since there are 7 days in a week
    timeLeft = (datetime.strptime(contestInfo['time'], "%H:%M") - datetime.strptime(current_time, "%H:%M:%S"))

    # If we have a negative number of days left, we need to adjust
    if timeLeft.days < 0:
        daysLeft -= 1
        timeLeft = timeLeft + datetime.timedelta(hours = 24)

    return [daysLeft, timeLeft]

out = getContestTime("biweekly")
print(f"{out[0]} days and {out[1]} hours left") 

out = getContestTime("weekly")
print(f"{out[0]} days and {out[1]} hours left") 

####################################################################################### NOTES / FIXES
# This is throwing an error one weekly objects when its giving back -1
# This also doesnt account for how biweekly contests can be more than 7 days away.