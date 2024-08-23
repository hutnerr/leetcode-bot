import datetime

def increaseContestNum(contestfile):
    with open(contestfile, 'r+') as f:
        num = int(f.readline()) + 1
        f.seek(0)
        f.write(str(num))

