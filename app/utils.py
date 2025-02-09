import hashlib

# Función para hashear la contraseña
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# Función para verificar la contraseña
def check_password(password: str, hashed_password: str) -> bool:
    return hash_password(password) == hashed_password
