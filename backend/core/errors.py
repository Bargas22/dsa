class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class ValidationError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 400)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Autenticação necessária."):
        super().__init__(message, 401)


class NotFoundError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 404)


class ConflictError(AppError):
    def __init__(self, message: str):
        super().__init__(message, 409)
