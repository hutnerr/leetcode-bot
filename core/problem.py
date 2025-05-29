class Problem:

    def __init__(self, pid: int, sid: int, difs: str, dow: int, hour: int, interval: int):
        self.problemID: int = pid
        self.serverID: int = sid
        # easy,med,hard...
        self.difficulties: list[str] = difs.split(",") if difs else None
        self.dow: int = dow  # 1 - 7
        self.hour: int = hour  # 0 - 23
        # interval can be 0, 1, 2, 3. 0=0min 1=15min, 2=30min, 3=45min
        self.interval: int = interval

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

    def toJSON(self) -> dict:
        return {
            "problemID": self.problemID,
            "serverID": self.serverID,
            "difficulties": self.difficulties,
            "dow": self.dow,
            "hour": self.hour,
            "interval": self.interval
        }

    # ===================================
    # helper functions
    # ===================================

    @staticmethod
    def titleToSlug(title: str) -> str:
        return title.replace(" ", "-").lower()

    @staticmethod
    def buildFromJSON(data: dict) -> "Problem":
        return Problem(
            pid=data["problemID"],
            sid=data["serverID"],
            difs=",".join(data["difficulties"]) if data["difficulties"] else "",
            dow=data["dow"],
            hour=data["hour"],
            interval=data["interval"]
        )