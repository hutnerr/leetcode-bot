from utils import json_helper as jsonh
import os

class User:
    def __init__(self, discordID: int, leetcodeUsername=None, points=0):
        self.discordID = discordID
        self.leetcodeUsername = leetcodeUsername
        self.points = points
        
    def __str__(self) -> str:
        return (f"User("
                f"discordID={self.discordID}, "
                f"leetcodeUsername={self.leetcodeUsername}, "
                f"points={self.points})")
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def setLeetCodeUsername(self, username: str):
        self.leetcodeUsername = username.strip()
        self.toJSON()
    
    def addPoints(self, points: int):
        self.points += points
        self.toJSON()
    
    def toJSON(self) -> dict:
        data =  {
            "discordID": self.discordID,
            "leetcodeUsername": self.leetcodeUsername,
            "points": self.points
        }
        jsonh.writeJSON(f"{os.path.join('data', 'users', f'{self.discordID}.json')}", data)

    @staticmethod
    def buildFromJSON(data: dict) -> "User":
        return User(
            discordID=data["discordID"],
            leetcodeUsername=data["leetcodeUsername"],
            points=data["points"]
        )