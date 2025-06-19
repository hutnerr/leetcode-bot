# will be used when a user requires admin permissions but does not have them
class AdminCheckException(Exception):
    def __init__(self, message = "User does not have admin privileges"):
        self.message = message
        super().__init__(self.message)