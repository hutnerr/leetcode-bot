# will be used when a user requires admin permissions but does not have them
class SimpleException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)