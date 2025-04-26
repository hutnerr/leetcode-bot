from utils import logger

class Problem:
        
    def __init__(self, pid:int, sid:int, difs:str, dow:int, hour:int, interval:int):
        self.problemID:int = pid
        self.serverID:int = sid
        self.difficulties:list[str] = difs.split(",") if difs else None # easy,med,hard...
        self.dow:int = dow # 1 - 7
        self.hour:int = hour # 0 - 23
        self.interval:int = interval # interval can be 0, 1, 2, 3. 0=0min 1=15min, 2=30min, 3=45min
        
    def __str__(self) -> str:
        return (f"Problem("
                f"problemID={self.problemID}, "
                f"serverID={self.serverID}, "
                f"difficulties={self.difficulties}, "
                f"dow={self.dow}, "
                f"hour={self.hour}, "
                f"interval={self.interval})")

    def __repr__(self) -> str:
        return self.__str__()

    # builds what will be the dict key
    # splittable by :: later
    def getKey(self) -> str:
        return f"{self.serverID}::{self.problemID}"
    
    def toCSV(self) -> str:
        # replace , with --- in difficulties so i can store the whole thing in a csv
        temp = "---".join(self.difficulties)
        return f"{self.problemID},{self.serverID},{temp},{self.dow},{self.hour},{self.interval}"

def problemFromCSV(line:str) -> "Problem":
    split = line.split(",")
    try:
        return Problem(
            int(split[0]), # problem id
            int(split[1]), # server id
            split[2].replace("-", ","), # difficulties
            int(split[3]), # day of week
            int(split[4]), # hour
            int(split[5])  # interval
        )
    except Exception as e:
        logger.error(f"Error reading problem from csv: {line} {e}")
    
def titleToSlug(title:str) -> str:
    return title.replace(" ", "-").lower()