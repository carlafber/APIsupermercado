from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/categorias",  # Prefijo en las rutas de categoria
    tags=["Categorías"],  # Esta etiqueta agrupa las rutas en Swagger UI
)

@router.get("/")
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

@router.post("/", response_model=schemas.Categoria)
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


@router.get("/{categoria_id}", response_model=schemas.Categoria)
def obtener_categoria(categoria_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una categoría por su ID.
    - **categoria_id**: El ID de la categoría a buscar.
    """
    return db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
