class Problem:
        
    def __init__(self, pid, sid, difs, dow, hour, interval):
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