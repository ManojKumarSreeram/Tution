class CustomAPIException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
class BadRequestException(CustomAPIException):
    def __init__(self, message="Bad request"):
        super().__init__(message, status_code=400)

class UnauthorizedException(CustomAPIException):
    def __init__(self, message="Unauthorized"):
        super().__init__(message, status_code=401)

class ForbiddenException(CustomAPIException):
    def __init__(self, message="Forbidden"):
        super().__init__(message, status_code=403)

class NotFoundException(CustomAPIException):
    def __init__(self, message="Not Found"):
        super().__init__(message, status_code=404)

class InternalServerError(CustomAPIException):
    def __init__(self, message="Internal Server Error"):
        super().__init__(message, status_code=500)
