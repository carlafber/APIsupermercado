from datetime import datetime
from http.client import HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app import models, schemas
from app.exceptions import NotFoundException

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


@router.get("/{id}", response_model=schemas.ListaCompraResponse, summary="Obtener lista de la compra por id")
def obtener_lista_compra(id: int, db: Session = Depends(get_db)):
    """
    Obtiene una lista de compra por su ID.
    - **id**: El ID de la lista de compra.
    """
    lista_compra = db.query(models.ListaCompra).filter(models.ListaCompra.id == id).first()
    if not lista_compra:
        return {"message": "Lista de compra no encontrada"}

    productos_lista = db.query(models.ProductoLista).filter(models.ProductoLista.lista_compra_id == id).all()
    
    lista_compra_response = schemas.ListaCompraResponse(
        id=lista_compra.id,
        fecha_creacion=lista_compra.fecha_creacion,
        productos=[schemas.ProductoLista(
            producto=producto.producto.nombre,
            cantidad=producto.cantidad,
            precio=producto.precio
        ) for producto in productos_lista]
    )
    return lista_compra_response


@router.get("/{id}/productos", summary="Buscar productos de una lista")
def obtener_productos_lista(id: int, db: Session = Depends(get_db)):
    productos_lista = (
        db.query(models.ProductoLista)
        .filter(models.ProductoLista.lista_compra_id == id)
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


@router.post("/nueva", summary="Crear nueva lista")
def crear_lista_compra(lista_compra: schemas.ListaCompraRespNueva, db: Session = Depends(get_db)):
    """
    Crea una nueva lista de compra.
    - **supermercado**: El nombre del supermercado donde se compra.
    - **usuario**: El nombre de la lista de compra.
    """

    # Buscar el supermercado por nombre
    if lista_compra.supermercado:
        supermercado_db = db.query(models.Supermercado).filter(models.Supermercado.nombre == lista_compra.supermercado).first()
        if supermercado_db:
            supermercado_id = supermercado_db.id
        else:
            raise NotFoundException(detail="Supermercado no encontrado")
    else:
        raise NotFoundException(detail="El supermercado es obligatorio")
    

    # Buscar el usuario por nombre
    if lista_compra.usuario:
        usuario_db = db.query(models.Usuario).filter(models.Usuario.nombre == lista_compra.usuario).first()
        if usuario_db:
            usuario_id = usuario_db.id
        else:
            raise NotFoundException(detail="Usuario no encontrado")
    else:
        raise NotFoundException(detail="El usuario es obligatorio")


    db_lista_compra = models.ListaCompra(
        supermercado_id=supermercado_id,
        usuario_id=usuario_id,
        fecha_creacion=datetime.now()
    )
    db.add(db_lista_compra)
    db.commit()
    db.refresh(db_lista_compra)

    return {"mensaje": "Lista de la compra creada exitosamente"}


@router.post("/{lista_compra_id}/producto", summary="Agregar un producto a una lista de compra")
def agregar_producto_a_lista(lista_compra_id: int, nombre_producto: str, cantidad: int, db: Session = Depends(get_db)):
    """
    Agrega un producto a una lista de compra existente usando el nombre del producto.
    - **lista_compra_id**: ID de la lista de compra a la que se agregará el producto.
    - **nombre_producto**: Nombre del producto a agregar.
    - **cantidad**: Cantidad del producto.
    """
    
    # Buscar la lista de compra
    lista_compra = db.query(models.ListaCompra).filter(models.ListaCompra.id == lista_compra_id).first()

    if not lista_compra:
        raise NotFoundException(detail="Lista de compra no encontrada")

    # Obtener el producto por nombre
    producto = db.query(models.Producto).filter(models.Producto.nombre == nombre_producto).first()

    if not producto:
        raise NotFoundException(detail="Producto no encontrado")

    # Verificar si el producto ya está en la lista de compra
    producto_lista = db.query(models.ProductoLista).filter(
        models.ProductoLista.lista_compra_id == lista_compra_id,
        models.ProductoLista.producto_id == producto.id  # Usar el ID del producto obtenido
    ).first()

    if producto_lista:
        raise NotFoundException(detail="El producto ya está en la lista de compra")

    # Calcular el precio del producto (asumimos que el precio se encuentra en el campo 'precio' del modelo Producto)
    precio = producto.precio

    # Agregar el producto a la lista de compra
    nuevo_producto_lista = models.ProductoLista(
        lista_compra_id=lista_compra_id,
        producto_id=producto.id,
        cantidad=cantidad,
        precio=precio*cantidad
    )

    db.add(nuevo_producto_lista)
    db.commit()
    db.refresh(nuevo_producto_lista)  # Actualizar el objeto para reflejar los datos de la base de datos
    
    return {"message": "Producto agregado a la lista de compra"}



@router.delete("/eliminar/{id}", summary="Eliminar una lista de compra")
def eliminar_lista_compra(id: int, db: Session = Depends(get_db)):
    """
    Elimina una lista de compra por su ID.
    - **lista_compra_id**: ID de la lista de compra a eliminar.
    """
    lista_compra = db.query(models.ListaCompra).filter(models.ListaCompra.id == id).first()

    if not lista_compra:
        return {"message": "Lista de compra no encontrada"}

    # Eliminar los productos de la lista
    db.query(models.ProductoLista).filter(models.ProductoLista.lista_compra_id == id).delete()

    # Eliminar la lista de compra
    db.delete(lista_compra)
    db.commit()

    return {"mensaje": "Lista de compra eliminada con éxito"}

