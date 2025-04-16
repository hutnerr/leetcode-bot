"""
Error for admin permission checks in discord. 
"""
class NotAdminError(Exception):
    """
    Exception raised for errors in the admin access.
    """
    def __init__(self, message = "User does not have admin privileges"):
        self.message = message
        super().__init__(self.message)