class ServerSettings:
    
    def __init__(self):
        self.test = "test_value"
    
    def toJSON(self) -> dict:
        return {
            "test": self.test,
        }
    
    def __str__(self) -> str:
        return "TESTING"
    
    @staticmethod
    def buildFromJSON() -> "ServerSettings":
        return ServerSettings()