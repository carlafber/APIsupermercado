from fastapi import HTTPException

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Recurso no encontrado"):
        super().__init__(status_code=404, detail=detail)

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "No autorizado"):
        super().__init__(status_code=401, detail=detail)

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Acceso denegado"):
        super().__init__(status_code=403, detail=detail)

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Solicitud incorrecta"):
        super().__init__(status_code=400, detail=detail)

class InternalServerErrorException(HTTPException):
    def __init__(self, detail="Error interno del servidor"):
        super().__init__(status_code=500, detail=detail)