import datetime

def increaseContestNum(contestfile):
    with open(contestfile, 'r+') as f:
        num = int(f.readline()) + 1
        f.seek(0)
        f.write(str(num))

def getContestTime():
    current_time = datetime.datetime.now()
    est_time = current_time.astimezone(datetime.timezone(datetime.timedelta(hours=-5)))  # Convert current time to EST
    edt_time = datetime.datetime.strptime("2024-08-24 10:30:00", "%Y-%m-%d %H:%M:%S")  # Replace with your specific time in EDT
    time_difference = edt_time - est_time
    print("Time difference:", time_difference)

getContestTime()