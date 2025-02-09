from sqlalchemy import *
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

# Tabla de Supermercados
class Supermercado(Base):
    __tablename__ = "supermercado"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, unique=True, nullable=False)

    productos = relationship("Producto", back_populates="supermercado", cascade="all, delete-orphan")
    listas_compra = relationship("ListaCompra", back_populates="supermercado", cascade="all, delete-orphan")


# Tabla de Categorías (Pasillos)
class Categoria(Base):
    __tablename__ = "categoria"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False)
    pasillo = Column(Integer, nullable=False)

    # Relación con Productos usando back_populates
    productos = relationship("Producto", back_populates="categoria", cascade="all, delete-orphan")


# Tabla de Productos
class Producto(Base):
    __tablename__ = "producto"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String)
    precio = Column(Float)
    supermercado_id = Column(Integer, ForeignKey("supermercado.id"))
    categoria_id = Column(Integer, ForeignKey("categoria.id"))

    # Relación con Categoria usando back_populates
    categoria = relationship("Categoria", back_populates="productos")

    # Relación con ProductoLista usando back_populates
    producto_lista = relationship("ProductoLista", back_populates="producto", cascade="all, delete-orphan")

    # Relación con Supermercado usando back_populates
    supermercado = relationship("Supermercado", back_populates="productos")


# Tabla ListaCompra
class ListaCompra(Base):
    __tablename__ = "lista_compra"
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    supermercado_id = Column(Integer, ForeignKey("supermercado.id"))
    usuario_id = Column(Integer, ForeignKey("usuario.id"))

    # Relación con Supermercado usando back_populates
    supermercado = relationship("Supermercado", back_populates="listas_compra")
    usuario = relationship("Usuario", back_populates="listas_compra")
    productos = relationship("ProductoLista", back_populates="lista_compra", cascade="all, delete-orphan")


# Tabla ProductoLista (relación entre productos y listas de compra)
class ProductoLista(Base):
    __tablename__ = "producto_lista"
    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, default=1)
    precio = Column(Float)
    lista_compra_id = Column(Integer, ForeignKey("lista_compra.id"))
    producto_id = Column(Integer, ForeignKey("producto.id"))

    # Relación con ListaCompra usando back_populates
    lista_compra = relationship("ListaCompra", back_populates="productos")
    
    # Relación con Producto usando back_populates
    producto = relationship("Producto", back_populates="producto_lista")


# Tabla de Usuarios
class Usuario(Base):
    __tablename__ = "usuario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)

    listas_compra = relationship("ListaCompra", back_populates="usuario")