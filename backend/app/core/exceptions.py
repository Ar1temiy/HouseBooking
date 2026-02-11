from __future__ import annotations


class AppError(Exception):
    status_code: int = 400
    detail: str = "Bad request"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail


class BadRequestError(AppError):
    status_code = 400
    detail = "Bad request"


class UnauthorizedError(AppError):
    status_code = 401
    detail = "Unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    detail = "Forbidden"


class NotFoundError(AppError):
    status_code = 404
    detail = "Not found"


class ConflictError(AppError):
    status_code = 409
    detail = "Conflict"
