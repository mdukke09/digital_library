import re

def is_password_valid(password: str) -> bool:
    """
    Valida que la contraseña cumpla con los requisitos mínimos:
    - Al menos 8 caracteres
    - Al menos una mayúscula
    - Al menos una minúscula
    - Al menos un número
    """
    if len(password) < 8:
        return False
    if not any(c.isupper() for c in password):
        return False
    if not any(c.islower() for c in password):
        return False
    if not any(c.isdigit() for c in password):
        return False
    return True