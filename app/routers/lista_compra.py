from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/listas_compra",  # Prefijo en las rutas de listas de compra
    tags=["Listas de Compra"],  # Esta etiqueta agrupa las rutas en Swagger UI
)

@router.get("/")
def obtener_listas_compra(db:Session=Depends(get_db)):
    data = db.query(models.ListaCompra).all()

    # Construimos la respuesta con detalles de la lista
    resultado = [
        {
            "id": item.id,
            "usuario": item.usuario.nombre,
            "fecha": item.fecha_creacion.strftime('%d-%m-%Y'),
            "supermercado": item.supermercado.nombre,
            "productos": len(item.productos),
        }
        for item in data
    ]

    return resultado 

@router.post("/", response_model=schemas.ListaCompra)
def crear_lista_compra(lista_compra: schemas.ListaCompra, db: Session = Depends(get_db)):
    """
    Crea una nueva lista de compra.
    - **supermercado_id**: El ID del supermercado donde se compra.
    - **nombre**: El nombre de la lista de compra.
    - **fecha_creacion**: La fecha de creación de la lista de compra.
    """
    db_lista_compra = models.ListaCompra(
        supermercado_id=lista_compra.supermercado_id,
        nombre=lista_compra.nombre,
        fecha_creacion=lista_compra.fecha_creacion
    )
    db.add(db_lista_compra)
    db.commit()
    db.refresh(db_lista_compra)
    return db_lista_compra


@router.get("/{lista_compra_id}", response_model=schemas.ListaCompraResponse)
def obtener_lista_compra(lista_compra_id: int, db: Session = Depends(get_db)):
    """
    Obtiene una lista de compra por su ID.
    - **lista_compra_id**: El ID de la lista de compra.
    """
    lista_compra = db.query(models.ListaCompra).filter(models.ListaCompra.id == lista_compra_id).first()
    if not lista_compra:
        return {"message": "Lista de compra no encontrada"}

    productos_lista = db.query(models.ProductoLista).filter(models.ProductoLista.lista_compra_id == lista_compra_id).all()
    
    lista_compra_response = schemas.ListaCompraResponse(
        id=lista_compra.id,
        nombre=lista_compra.nombre,
        fecha_creacion=lista_compra.fecha_creacion,
        productos=[schemas.ProductoLista(
            id=producto.id,
            lista_compra_id=producto.lista_compra_id,
            producto_id=producto.producto_id,
            cantidad=producto.cantidad,
            precio=producto.precio
        ) for producto in productos_lista]
    )
    return lista_compra_response

@router.get("/{lista_id}/productos")
def obtener_productos_lista(lista_id: int, db: Session = Depends(get_db)):
    productos_lista = (
        db.query(models.ProductoLista)
        .filter(models.ProductoLista.lista_compra_id == lista_id)
        .all()
    )
    
    # Construimos la respuesta con detalles del producto
    resultado = [
        {
            "id": item.producto.id,
            "nombre": item.producto.nombre,
            "cantidad": item.cantidad,
            "precio": item.precio
        }
        for item in productos_lista
    ]

    return resultado