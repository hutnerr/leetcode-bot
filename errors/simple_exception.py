class SimpleException(Exception):
    def __init__(self, code, message, help = None):
        self.code = code
        self.message = message
        self.help = help if help else "Likely a backend issue. Apologies for any inconvenience. Please try again later."
        super().__init__(self.message)