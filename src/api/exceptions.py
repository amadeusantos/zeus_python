class CoreException(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(self.message)

class NotAuthenticatedException(CoreException):
    def __init__(self):
        super().__init__(401, "Not authenticated")

class TokenInvalidException(CoreException):
    def __init__(self):
        super().__init__(401, "Token is invalid or expired")

class ForbiddenException(CoreException):
    def __init__(self):
        super().__init__(403, "User not authorized")