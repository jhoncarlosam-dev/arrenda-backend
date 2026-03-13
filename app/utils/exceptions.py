from fastapi import HTTPException, status
from typing import Any, Dict, Optional

class APIException(HTTPException):
    def __init__(
        self,
        status_code: int,
        message: str,
        data: Optional[Any] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        super().__init__(status_code=status_code, detail=message, headers=headers)
        self.data = data
        self.message = message

class BadRequestException(APIException):
    def __init__(self, message: str = "Bad Request", data: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, message=message, data=data)

class UnauthorizedException(APIException):
    def __init__(self, message: str = "Unauthorized", data: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, message=message, data=data)

class ForbiddenException(APIException):
    def __init__(self, message: str = "Forbidden", data: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, message=message, data=data)

class NotFoundException(APIException):
    def __init__(self, message: str = "Not Found", data: Optional[Any] = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, message=message, data=data)
