from ..exceptions import CoreException


class RoleNotFoundException(CoreException):
    def __init__(self):
        super().__init__(status_code=404, message="Role not found")


class RoleNameAlreadyExistsException(CoreException):
    def __init__(self):
        super().__init__(status_code=409, message="Role name already exists")