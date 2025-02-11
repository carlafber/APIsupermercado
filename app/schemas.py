from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Esquema de Usuario
class Usuario(BaseModel):
    username: str
    password: str
    nombre: str
    apellido: str

# Esquema de Producto
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    supermercado_id: int
    categoria_id: int

    class Config:
        orm_mode = True

# Esquema de Supermercado
class Supermercado(BaseModel):
    nombre: str

# Esquema de Categoría
class Categoria(BaseModel):
    nombre: str
    pasillo: int

# Esquema de ProductoLista
class ProductoLista(BaseModel):
    producto: str
    cantidad: int
    precio: float

    class Config:
        orm_mode = True

# Esquema de ListaCompra
class ListaCompra(BaseModel):
    id: int
    supermercado_id: int
    fecha_creacion: datetime

    class Config:
        orm_mode = True

# Esquema de ListaCompra
class ListaCompraRespNueva(BaseModel):
    supermercado: str
    usuario: str

    class Config:
        orm_mode = True

# Esquema de Respuesta de Producto (ProductoResponse)
class ProductoResponse(BaseModel):
    nombre: str
    precio: float
    supermercado: str
    categoria: str

    class Config:
        orm_mode = True

# Esquema de Respuesta de Producto (ProductoResponse)
class ProductoRespActCat(BaseModel):
    nombre: str
    categoria: str

    class Config:
        orm_mode = True

# Esquema de Respuesta de Producto (ProductoResponse)
class ProductoRespActPre(BaseModel):
    precio: float

    class Config:
        orm_mode = True

# Esquema para obtener los productos en una lista de compra
class ListaCompraResponse(BaseModel):
    id: int
    fecha_creacion: datetime
    productos: List[ProductoLista]

    class Config:
        orm_mode = True
