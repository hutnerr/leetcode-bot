# representation of a leetcode problem settings
# used by servers 
# stores information to determine what type of problem & when it should be sent
class Problem:

    def __init__(self, pid: int, sid: int, difs: str, dow: int, hour: int, interval: int, premium: int):
        self.problemID: int = pid
        self.serverID: int = sid
        self.difficulties: list[str] = difs.split("-") if difs else None # easy,med,hard...
        self.dow: int = dow  # 1 - 7
        self.hour: int = hour  # 0 - 23
        self.interval: int = interval  # interval can be 0, 1, 2, 3. 0=0min 1=15min, 2=30min, 3=45min
        self.premium: int = premium  # 0=free, 1=premium, 2=either

    def __str__(self) -> str:
        return (f"Problem("
                f"problemID={self.problemID}, "
                f"serverID={self.serverID}, "
                f"difficulties={self.difficulties}, "
                f"dow={self.dow}, "
                f"hour={self.hour}, "
                f"interval={self.interval}, "
                f"premium={self.premium})")

    def __repr__(self) -> str:
        return self.__str__()

    def __compare__(self, other: "Problem") -> bool:
        if not isinstance(other, Problem):
            return False
        return (self.problemID == other.problemID and
                self.serverID == other.serverID and
                self.difficulties == other.difficulties and
                self.dow == other.dow and
                self.hour == other.hour and
                self.interval == other.interval and
                self.premium == other.premium)

    # builds what will be the dict key
    # splittable by :: later
    def getKey(self) -> str:
        return f"{self.serverID}::{self.problemID}"

    def toJSON(self) -> dict:
        return {
            "problemID": self.problemID,
            "serverID": self.serverID,
            "difficulties": self.difficulties,
            "dow": self.dow,
            "hour": self.hour,
            "interval": self.interval,
            "premium": self.premium
        }

    # ===================================
    # helper functions
    # ===================================

    @staticmethod
    def buildFromJSON(data: dict) -> "Problem":
        return Problem(
            pid=data["problemID"],
            sid=data["serverID"],
            difs="-".join(data["difficulties"]
                          ) if data["difficulties"] else "",
            dow=data["dow"],
            hour=data["hour"],
            interval=data["interval"],
            premium=data["premium"]
        )
