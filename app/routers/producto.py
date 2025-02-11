from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.exceptions import NotFoundException
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


@router.get("/buscar", summary="Buscar productos con un filtro")
def obtener_productos_filtro(supermercado_id: int, categoria_id: int, db: Session = Depends(get_db)):

    """
    Buscar poroductos filtrando por supermercado y categoría.
    - **supermercado_id**: Id del supermercado.
    - **categoria_id**: Id de la categoría.
    """

    # Realizar la consulta que incluye la relación con la categoría
    productos = db.query(models.Producto).join(models.Categoria).filter(
        models.Producto.supermercado_id == supermercado_id,
        models.Producto.categoria_id == categoria_id
    ).all()

    # Transformar los productos para incluir el nombre y pasillo de la categoría
    resultado = []
    for producto in productos:
        categoria = db.query(models.Categoria).filter(models.Categoria.id == producto.categoria_id).first()
        resultado.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "pasillo": categoria.pasillo,
            "categoria": categoria.nombre,
            "supermercado": producto.supermercado.nombre
        })
    
    return resultado


@router.get("/ordenados", summary="Obtener productos ordenados")
def obtener_productos_ordenados(orden: str = "nombre", db: Session = Depends(get_db)):
    """
    Obtiene todos los productos ordenados.
    - **orden**: Puede ser "nombre" o "precio".
    """
    if orden not in ["nombre", "precio"]:
        return {"error": "Parámetro de orden inválido. Usa 'nombre' o 'precio'."}

    productos = db.query(models.Producto).order_by(getattr(models.Producto, orden)).all()

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
        for item in productos
    ]

    return resultado


@router.get("/filtrar/precio", summary="Filtrar productos por precio")
def filtrar_productos_por_precio(min_precio: float, max_precio: float, db: Session = Depends(get_db)):
    """
    Filtra productos dentro de un rango de precios.
    - **min_precio**: Precio mínimo.
    - **max_precio**: Precio máximo.
    """
    productos = db.query(models.Producto).filter(
        models.Producto.precio >= min_precio,
        models.Producto.precio <= max_precio
    ).all()

    if not productos:
        return {"error": "No se encontraron productos en ese rango de precios"}


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
        for item in productos
    ]

    return resultado


@router.post("/nuevo", summary="Crear un nuevo producto")
def crear_producto(producto: schemas.ProductoResponse, db: Session = Depends(get_db)):
    """
    Crea un nuevo producto en el sistema.
    - **nombre**: Nombre del producto.
    - **precio**: Precio del producto.
    - **supermercado**: Nombre del supermercado donde se vende el producto.
    - **categoria**: Nombre de la categoría del producto.
    """

    # Buscar el supermercado por nombre
    if producto.supermercado:
        supermercado_db = db.query(models.Supermercado).filter(models.Supermercado.nombre == producto.supermercado).first()
        if supermercado_db:
            supermercado_id = supermercado_db.id
        else:
            raise NotFoundException(detail="Supermercado no encontrado")
    else:
        raise NotFoundException(detail="El supermercado es obligatorio")

    # Buscar la categoría por nombre
    if producto.categoria:
        categoria_db = db.query(models.Categoria).filter(models.Categoria.nombre == producto.categoria).first()
        if categoria_db:
            categoria_id = categoria_db.id
        else:
            raise NotFoundException(detail="Categoría no encontrada")
    else:
        raise NotFoundException(detail="La categoría es obligatoria")

    # Crear el nuevo producto
    nuevo_producto = models.Producto(
        nombre=producto.nombre,
        precio=producto.precio,
        supermercado_id=supermercado_id,
        categoria_id=categoria_id
    )

    # Agregar el producto a la base de datos y hacer commit
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)

    return {"mensaje": "Producto creado exitosamente"}


@router.put("/actualizar-categoria/{id}", summary="Actualizar la categoría de un producto")
def actualizar_producto(id: int, producto: schemas.ProductoRespActCat, db: Session = Depends(get_db)):
    """
    Actualiza la categoría de un producto por su ID.
    - **categoria**: Nombre de la nueva categoría del producto.
    """
    # Buscar el producto en la base de datos
    producto_buscado = db.query(models.Producto).filter(models.Producto.id == id).first()

    # Verificar si el producto existe
    if producto_buscado is None:
        raise NotFoundException(detail="Producto no encontrado")


    if producto.categoria:
        # Buscar la categoría por nombre
        categoria_db = db.query(models.Categoria).filter(models.Categoria.nombre == producto.categoria).first()
        if categoria_db:
            producto_buscado.categoria_id = categoria_db.id
        else:
            raise NotFoundException(detail="Categoría no encontrada")

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(producto_buscado)

    return {"mensaje": "Producto actualizado con éxito"}



@router.put("/actualizar-precio/{id}", summary="Actualizar el precio de un producto")
def actualizar_precio_producto(id: int, producto: schemas.ProductoRespActPre, db: Session = Depends(get_db)):
    """
    Actualiza el precio de un producto por su ID.
    - **id**: ID del producto a actualizar.
    - **nuevo_precio**: Nuevo precio del producto.
    """
    # Buscar el producto en la base de datos
    producto_db = db.query(models.Producto).filter(models.Producto.id == id).first()

    # Verificar si el producto existe
    if producto_db is None:
        raise NotFoundException(detail="Producto no encontrado")

    # Actualizar el precio del producto
    producto_db.precio = producto.precio

    # Guardar los cambios en la base de datos
    db.commit()
    db.refresh(producto_db)

    return {"mensaje": "Precio del producto actualizado con éxito"}


@router.delete("/eliminar/{id}", summary="Eliminar un producto")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    """
    Elimina un producto por su ID.
    - **id**: ID del producto a eliminar.
    """
    producto_db = db.query(models.Producto).filter(models.Producto.id == id).first()

    if not producto_db:
        return {"error": "Producto no encontrado"}

    db.delete(producto_db)
    db.commit()

    return {"mensaje": "Producto eliminado con éxito"}
