from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas

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


@router.get("/buscar/{id}", response_model=schemas.Categoria, summary="Obtener todas las categorías")
def obtener_categoria(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoría por su ID.
    - **id**: El ID de la categoría a buscar.
    """
    return db.query(models.Categoria).filter(models.Categoria.id == id).first()


@router.post("/nueva", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.Categoria, db: Session = Depends(get_db)):
    """
    Crea una nueva categoría en el sistema.
    - **nombre**: Nombre de la categoría.
    - **pasillo**: El pasillo del supermercado donde se encuentra la categoría.
    """
    db_categoria = models.Categoria(nombre=categoria.nombre, pasillo=categoria.pasillo)
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria


