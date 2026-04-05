from ..exceptions import CoreException


class InvalidCredentialsException(CoreException):
    def __init__(self):
        super().__init__(status_code=401, message="Invalid email or password")

class UserInactiveException(CoreException):
    def __init__(self):
        super().__init__(status_code=403, message="User account is inactive")