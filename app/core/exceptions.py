from fastapi import HTTPException
from typing import Any

class NotFoundError(HTTPException):
    """Error para recursos no encontrados"""
    def __init__(self, detail: Any = None):
        super().__init__(status_code=404, detail=detail or "Recurso no encontrado")

class ValidationError(HTTPException):
    """Error para validación de datos"""
    def __init__(self, detail: Any = None):
        super().__init__(status_code=422, detail=detail or "Error de validación")

class AuthenticationError(HTTPException):
    """Error para problemas de autenticación"""
    def __init__(self, detail: Any = None):
        super().__init__(status_code=401, detail=detail or "Error de autenticación")

class AuthorizationError(HTTPException):
    """Error para problemas de autorización"""
    def __init__(self, detail: Any = None):
        super().__init__(status_code=403, detail=detail or "No autorizado")