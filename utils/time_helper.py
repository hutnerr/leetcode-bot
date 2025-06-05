def minutesToHours(minutes: int) -> str:
    if minutes < 0:
        return "INVALID INPUT"

    hours = int(minutes // 60)
    remMins = int(minutes % 60)

    timeString = ""
    if hours == 0 and remMins == 0:
        return "0 minutes"

    if hours == 1:
        timeString += "1 hour"
    elif hours == 0:
        timeString += "" # do nothing
    else:
        timeString += f"{hours} hours"

    if hours > 0 and remMins > 0:
        timeString += " and "
    elif hours > 0 and remMins == 0:
        return timeString.strip()

    if remMins == 0:
        return timeString
    elif remMins == 1:
        timeString += "1 minute"
    else:
        timeString += f"{remMins} minutes"

    return timeString