from datetime import datetime
from app import models
from sqlalchemy.orm import Session

# Función para cargar datos iniciales
def cargar_bd(db: Session):
    # Insertar datos en la tabla Supermercado si está vacía
    if not db.query(models.Supermercado).first():
        supermercados = [
            models.Supermercado(nombre="Carrefour"),
            models.Supermercado(nombre="Aldi"),
            models.Supermercado(nombre="Lidl"),
            models.Supermercado(nombre="Gadis"),
            models.Supermercado(nombre="Alcampo"),
            models.Supermercado(nombre="Dia"),
            models.Supermercado(nombre="Mercadona"),
            models.Supermercado(nombre="Alimerka"),
            models.Supermercado(nombre="Lupa"),
            models.Supermercado(nombre="Froiz")
        ]
        db.add_all(supermercados)
        db.commit()

    # Insertar datos en la tabla Categoria si está vacía
    if not db.query(models.Categoria).first():
        categorias = [
            models.Categoria(nombre="Frutas", pasillo=1),
            models.Categoria(nombre="Verduras", pasillo=2),
            models.Categoria(nombre="Bebidas", pasillo=3),
            models.Categoria(nombre="Lácteos", pasillo=4),
            models.Categoria(nombre="Carnes", pasillo=5),
            models.Categoria(nombre="Panadería", pasillo=6),
            models.Categoria(nombre="Congelados", pasillo=7),
            models.Categoria(nombre="Dulces", pasillo=8),
            models.Categoria(nombre="Aseo", pasillo=9),
            models.Categoria(nombre="Ropa", pasillo=10)
        ]
        db.add_all(categorias)
        db.commit()

    # Insertar datos en la tabla Producto si está vacía
    if not db.query(models.Producto).first():
        productos = [
            models.Producto(nombre="Manzana", precio=10.5, supermercado_id=1, categoria_id=1),
            models.Producto(nombre="Lechuga", precio=3.0, supermercado_id=2, categoria_id=2),
            models.Producto(nombre="Jugo de Naranja", precio=5.0, supermercado_id=3, categoria_id=3),
            models.Producto(nombre="Leche", precio=2.5, supermercado_id=1, categoria_id=4),
            models.Producto(nombre="Pollo", precio=6.0, supermercado_id=2, categoria_id=5),
            models.Producto(nombre="Pan de Molde", precio=1.2, supermercado_id=3, categoria_id=6),
            models.Producto(nombre="Helado", precio=4.5, supermercado_id=1, categoria_id=7),
            models.Producto(nombre="Chocolate", precio=3.2, supermercado_id=2, categoria_id=8),
            models.Producto(nombre="Detergente", precio=1.8, supermercado_id=3, categoria_id=9),
            models.Producto(nombre="Camiseta", precio=15.0, supermercado_id=1, categoria_id=10),
            models.Producto(nombre="Pera", precio=12.0, supermercado_id=2, categoria_id=1),
            models.Producto(nombre="Tomate", precio=4.0, supermercado_id=3, categoria_id=2),
            models.Producto(nombre="Zumo de Uva", precio=5.5, supermercado_id=1, categoria_id=3),
            models.Producto(nombre="Yogurt", precio=2.8, supermercado_id=2, categoria_id=4),
            models.Producto(nombre="Carne de Res", precio=7.0, supermercado_id=3, categoria_id=5)
        ]
        db.add_all(productos)
        db.commit()

    # Insertar datos en la tabla Usuario si está vacía
    if not db.query(models.Usuario).first():
        usuarios = [
            models.Usuario(username="juan123", password="password123", nombre="Juan", apellido="Pérez"),
            models.Usuario(username="maria456", password="password456", nombre="Maria", apellido="López")
        ]
        db.add_all(usuarios)
        db.commit()

    # Insertar datos en la tabla ListaCompra si está vacía
    if not db.query(models.ListaCompra).first():
        lista_compra_1 = models.ListaCompra(
            fecha_creacion=datetime.utcnow(), supermercado_id=1, usuario_id=1
        )
        lista_compra_2 = models.ListaCompra(
            fecha_creacion=datetime.utcnow(), supermercado_id=2, usuario_id=2
        )
        lista_compra_3 = models.ListaCompra(
            fecha_creacion=datetime.utcnow(), supermercado_id=3, usuario_id=1
        )
        db.add_all([lista_compra_1, lista_compra_2, lista_compra_3])
        db.commit()

    # Insertar datos en la tabla ProductoLista si está vacía
    if not db.query(models.ProductoLista).first():
        producto_lista_1 = [
            models.ProductoLista(cantidad=3, precio=31.5, lista_compra_id=1, producto_id=1),
            models.ProductoLista(cantidad=2, precio=6.0, lista_compra_id=1, producto_id=2),
            models.ProductoLista(cantidad=4, precio=20.0, lista_compra_id=1, producto_id=3)
        ]
        producto_lista_2 = [
            models.ProductoLista(cantidad=2, precio=15.0, lista_compra_id=2, producto_id=4),
            models.ProductoLista(cantidad=1, precio=12.0, lista_compra_id=2, producto_id=5),
            models.ProductoLista(cantidad=3, precio=13.5, lista_compra_id=2, producto_id=6)
        ]
        producto_lista_3 = [
            models.ProductoLista(cantidad=5, precio=25.0, lista_compra_id=3, producto_id=7),
            models.ProductoLista(cantidad=2, precio=8.0, lista_compra_id=3, producto_id=8),
            models.ProductoLista(cantidad=1, precio=3.2, lista_compra_id=3, producto_id=9),
            models.ProductoLista(cantidad=3, precio=9.0, lista_compra_id=3, producto_id=10)
        ]
        db.add_all(producto_lista_1 + producto_lista_2 + producto_lista_3)
        db.commit()