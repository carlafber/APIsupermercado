from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas
from app.exceptions import NotFoundException

router = APIRouter(
    prefix="/supermercados",  # Prefijo en las rutas de supermercado
    tags=["Supermercados"],  # Esta etiqueta agrupa las rutas en Swagger UI
)

# Ruta para obtener todos los supermercados
@router.get("/", summary="Obtener todos los supermercados", description="Obtiene la lista de todos los supermercados registrados en el sistema.")
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


@router.get("/buscar/{id}", response_model=schemas.Supermercado)
def obtener_supermercado(id: int, db: Session = Depends(get_db)):
    """
    Obtiene un supermercado por su ID.
    - **id**: El ID del supermercado a buscar.
    """
    return db.query(models.Supermercado).filter(models.Supermercado.id == id).first()


@router.get("/listas/{id}", summary="Obtener listas de compra de un supermercado")
def obtener_listas_compra_supermercado(id: int, db: Session = Depends(get_db)):
    supermercado = db.query(models.Supermercado).filter(models.Supermercado.id == id).first()

    """
    Obtener las listas de la compra de un supermercado.
    - **id**: El ID del supermercado a filtrar.
    """

    if supermercado is None:
        raise NotFoundException(detail="Supermercado no encontrado")
    
    resultado = [
        {
            "id lista de la compra": item.id,
            "usuario": item.usuario.nombre,
            "fecha": item.fecha_creacion.strftime('%d-%m-%Y'),
            "supermercado": item.supermercado.nombre,
            "productos": len(item.productos),
        }
        for item in supermercado.listas_compra
    ]
    return resultado


@router.post("/nuevo", response_model=schemas.Supermercado, summary="Crear un nuevo supermercado")
def crear_supermercado(supermercado: schemas.Supermercado, db: Session = Depends(get_db)):
    """
    Crea un supermercado en el sistema.
    - **nombre**: Nombre del supermercado, asegúrate de usar uno que no exista.
    """
    nuevo_supermercado = models.Supermercado(nombre=supermercado.nombre)
    db.add(nuevo_supermercado)
    db.commit()
    db.refresh(nuevo_supermercado)

    return{"Respuesta": "Supermercado creado"}


@router.delete("/eliminar/{id}", summary="Eliminar un supermercado")
def eliminar_supermercado(id: int, db: Session = Depends(get_db)):
    """
    Eliminar un supermercado por su ID.
    - **id**: El ID del supermercado a eliminar.
    """

    supermercado = db.query(models.Supermercado).filter(models.Supermercado.id == id).first()
    if supermercado is None:
        raise NotFoundException(detail="Supermercado no encontrado")
    db.delete(supermercado)
    db.commit()
    return {"Respuesta": "Supermercado eliminado con éxito"}

