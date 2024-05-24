class TransactionTypeError(Exception):
    def __init__(self, message="Wrong transaction type"):
        self.message = message
        super().__init__(self.message)


class TransactionNonFound(Exception):
    def __init__(self, message="Transaction not found"):
        self.message = message
        super().__init__(self.message)
