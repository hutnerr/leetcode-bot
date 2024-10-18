from datetime import datetime

def timeDifference(then, now):
    return then - now

def distanceAway(then):
    return timeDifference(then, getCurrentTime())

def fromTimestamp(timestamp):
    return datetime.fromtimestamp(timestamp)

def getCurrentTime():
    return datetime.now()

def formatTime(time):
    return time.strftime("%A, %B %d, %Y %I:%M %p")

def timedeltaToDict(delta):
    timeDict = {
        "days" : delta.days,
        "hours" : delta.seconds // 3600,
        "minutes" : (delta.seconds // 60) % 60,
        "seconds" : delta.seconds % 60
    }
    
    return timeDict