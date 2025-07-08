import time

# converts an integer of minutes to a properly formatting string of hours / mins
def minutesToHours(minutes: int) -> str:
    if minutes < 0:
        return "INVALID INPUT"

    hours = int(minutes // 60)
    remMins = int(minutes % 60)

    timeString = ""
    if hours == 0 and remMins == 0:
        return "0 minutes"

    # build the hours portion
    if hours == 0:
        timeString += "" # do nothing
    elif hours == 1:
        timeString += "1 hour"
    else:
        timeString += f"{hours} hours"

    # should we add and or not?
    if hours > 0 and remMins > 0:
        timeString += " and "
    elif hours > 0 and remMins == 0:
        return timeString.strip()

    # build the mins portion
    if remMins == 0:
        return timeString
    elif remMins == 1:
        timeString += "1 minute"
    else:
        timeString += f"{remMins} minutes"

    return timeString

def getCurrentUNIXTime() -> int:
    return int(time.time())

def convertUnixToTime(unixTime: int) -> time.struct_time:
    return time.localtime(unixTime)

def calculateUnixTimeDifference(start: int, end: int) -> int:
    if start < 0 or end < 0:
        return -1
    return end - start

def formatTimeDelta(seconds: int) -> str:
    if seconds < 0:
        return "INVALID INPUT"
    if seconds == 0:
        return "0 seconds"

    weeks, seconds = divmod(seconds, 604800)  # 7*24*60*60
    days, seconds = divmod(seconds, 86400)    # 24*60*60
    hours, seconds = divmod(seconds, 3600)    # 60*60
    minutes, seconds = divmod(seconds, 60)

    parts = []
    if weeks > 0:
        parts.append(f"{weeks} week{'s' if weeks != 1 else ''}")
    if days > 0:
        parts.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")

    return ", ".join(parts)

def formatDateTime(timeStruct: time.struct_time) -> str:
    if not isinstance(timeStruct, time.struct_time):
        return "INVALID INPUT"
    
    return time.strftime("%A, %B %d at %I:%M %p", timeStruct).replace(" 0", " ").lstrip("0")


def numToDayOfWeek(num: int) -> str:
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    if 0 <= num < len(days):
        return days[num]
    return "INVALID DAY NUMBER"

def timeToEST() -> dict:
    pass