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