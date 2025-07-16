from exceptions import AppException


class InvalidInputError(AppException):
    def __init__(self, message="Invalid Input", status_code=400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UnauthorizedError(AppException):
    def __init__(self, message="Username or password incorrect", status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class InvalidJWTError(AppException):
    def __init__(self, message="Invalid JWT Token", status_code=401):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UrlNotFoundError(AppException):
    def __init__(self, message="URL Not found", status_code=404):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
