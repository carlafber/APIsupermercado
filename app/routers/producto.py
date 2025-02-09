from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas import Producto, Supermercado, Categoria
from app.db.database import get_db
from app import models

router = APIRouter(
    prefix="/productos",
    tags=["Productos"]
)

@router.get("/")
def obtener_productos(db:Session=Depends(get_db)):
    data = db.query(models.Producto).all()

    # Construimos la respuesta con detalles del producto
    resultado = [
        {
            "id": item.id,
            "nombre": item.nombre,
            "precio": item.precio,
            "pasillo": item.categoria.pasillo,
            "categoría": item.categoria.nombre,
            "supermercado": item.supermercado.nombre,
        }
        for item in data
    ]

    return resultado 

@router.post("/")
def crear_producto(producto: Producto, db: Session = Depends(get_db)):
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        supermercado_id=producto.supermercado_id,
        categoria_id=producto.categoria_id
    )
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"message": "Producto creado exitosamente"}


@router.get("/f")
def obtener_productos_filtro(supermercado_id: int, categoria_id: int, db: Session = Depends(get_db)):
    # Realizar la consulta que incluye la relación con la categoría
    productos = db.query(models.Producto).join(models.Categoria).filter(
        models.Producto.supermercado_id == supermercado_id,
        models.Producto.categoria_id == categoria_id
    ).all()

    # Transformar los productos para incluir el nombre y pasillo de la categoría
    result = []
    for producto in productos:
        categoria = db.query(models.Categoria).filter(models.Categoria.id == producto.categoria_id).first()
        result.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "pasillo": categoria.pasillo,
            "categoria": categoria.nombre,
            "supermercado": producto.supermercado.nombre
        })
    
    return result
