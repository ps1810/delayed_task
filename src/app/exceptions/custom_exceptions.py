from fastapi import HTTPException, status


class ModelValidationError(HTTPException):
    """The class is for handling validation error in request body of the /timer API"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )