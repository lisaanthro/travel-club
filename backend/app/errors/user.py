class EmailAlreadyAssociatedError(Exception):
    def __init__(self, message="This email is already associated with an account."):
        self.message = message
        super().__init__(self.message)


class AuthenticationError(Exception):
    def __init__(self, message="Invalid credentials"):
        self.message = message
        super().__init__(self.message)


class UserNotFoundError(Exception):
    def __init__(self, message="User not found"):
        self.message = message
        super().__init__(self.message)
