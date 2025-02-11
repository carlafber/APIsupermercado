from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import Usuario
from app.db.database import get_db
from app import models
from app.utils import hash_password, check_password

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

@router.get("/")
def obtener_usuarios(db:Session=Depends(get_db)):
    data = db.query(models.Usuario).all()
    
    # Construimos la respuesta con detalles del usuario
    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
            "apellido": item.apellido,
            "nombre de usuario": item.username,
            "contraseña": item.password,
        }
        for item in data
    ]

    return resultado

@router.post("/registrar")
def registrar_uusario(user: Usuario, db: Session = Depends(get_db)):
    # Encriptar la contraseña antes de guardarla
    hashed_password = hash_password(user.password)
    nuevo_usuario = models.Usuario(
        username=user.username,
        password=hashed_password,
        nombre=user.nombre,
        apellido=user.apellido,
    )
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return {"Respuesta": "Usuario creado exitosamente"}


@router.post("/login")
def login_user(user: Usuario, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.username == user.username).first()
    if usuario and check_password(user.password, usuario.password):
        return {"Respuesta": "Login exitoso"}
    raise HTTPException(status_code=401, detail="Credenciales inválidas")
