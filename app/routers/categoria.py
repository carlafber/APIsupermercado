from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas
from app.exceptions import NotFoundException

router = APIRouter(
    prefix="/categorias",  # Prefijo en las rutas de categoria
    tags=["Categorías"],  # Esta etiqueta agrupa las rutas en Swagger UI
)

@router.get("/", summary="Obtener todas las categorías", description="Obtiene la lista de todas las categorías registradas en el sistema.")
def obtener_categorias(db:Session=Depends(get_db)):
    data = db.query(models.Categoria).all()

    # Construimos la respuesta con detalles de la categoría
    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
            "pasillo": item.pasillo,
        }
        for item in data
    ]

    return resultado 


@router.get("/buscar/{id}", response_model=schemas.Categoria, summary="Buscar categoría")
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoría por su ID.
    - **id**: El ID de la categoría a buscar.
    """
    return db.query(models.Categoria).filter(models.Categoria.id == id).first()


@router.post("/nueva", summary="Crear una nueva categoría")
def crear_categoria(categoria: schemas.Categoria, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría en el sistema.
    - **nombre**: Nombre de la categoría.
    - **pasillo**: El pasillo del supermercado donde se encuentra la categoría.
    """
    nueva_categoria = models.Categoria(nombre=categoria.nombre, pasillo=categoria.pasillo)
    db.add(nueva_categoria)
    db.commit()
    db.refresh(nueva_categoria)
    return{"Respuesta": "Categoría creada"}


@router.put("/actualizar/{id}", summary="Actualizar una categoría")
def actualizar_categoria(id: int, categoria: schemas.Categoria, db: Session = Depends(get_db)):
    """
    Actualiza una categoría por su ID.
    - **id**: ID de la categoría a actualizar.
    - **nombre**: Nuevo nombre de la categoría.
    - **pasillo**: Nuevo número de pasillo.
    """
    categoria = db.query(models.Categoria).filter(models.Categoria.id == id).first()

    if categoria is None:
        raise NotFoundException(detail="Categoría no encontrada")

    categoria.nombre = categoria.nombre
    categoria.pasillo = categoria.pasillo

    db.commit()
    db.refresh(categoria)

    return {"mensaje": "Categoría actualizada con éxito"}


@router.delete("/eliminar/{id}", summary="Eliminar una categoría")
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    """
    Elimina una categoría por su ID.
    - **id**: ID de la categoría a eliminar.
    """
    categoria = db.query(models.Categoria).filter(models.Categoria.id == id).first()

    if categoria is None:
        raise NotFoundException(detail="Categoría no encontrada")

    db.delete(categoria)
    db.commit()

    return {"mensaje": "Categoría eliminada con éxito"}