from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/supermercados",  # Prefijo en las rutas de supermercado
    tags=["Supermercados"],  # Esta etiqueta agrupa las rutas en Swagger UI
)

@router.get("/")
def obtener_supermercados(db:Session=Depends(get_db)):
    data = db.query(models.Supermercado).all()

    # Construimos la respuesta con detalles del supermercado
    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
        }
        for item in data
    ]

    return resultado 

@router.post("/", response_model=schemas.Supermercado)
def crear_supermercado(supermercado: schemas.Supermercado, db: Session = Depends(get_db)):
    """
    Crea un supermercado en el sistema.
    - **nombre**: Nombre del supermercado.
    """
    nueva_supermercado = models.Supermercado(nombre=supermercado.nombre)
    db.add(nueva_supermercado)
    db.commit()
    db.refresh(nueva_supermercado)
    return nueva_supermercado


@router.get("/{supermercado_id}", response_model=schemas.Supermercado)
def obtener_supermercado(supermercado_id: int, db: Session = Depends(get_db)):
    """
    Obtiene un supermercado por su ID.
    - **supermercado_id**: El ID del supermercado a buscar.
    """
    return db.query(models.Supermercado).filter(models.Supermercado.id == supermercado_id).first()
