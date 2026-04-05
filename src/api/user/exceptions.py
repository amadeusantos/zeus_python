from ..exceptions import CoreException


class UserNotFoundException(CoreException):
    def __init__(self):
        super().__init__(status_code=404, message="User not found")


class UserEmailAlreadyExistsException(CoreException):
    def __init__(self):
        super().__init__(status_code=409, message="User email already exists")
