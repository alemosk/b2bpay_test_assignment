class InsufficientFundsException(Exception):
    def __init__(self, message='Insufficient funds for this operation',):
        self.message = message
        super().__init__(self.message)
