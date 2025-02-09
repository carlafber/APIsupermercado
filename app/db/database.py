from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#PUERTO DE CLASE -> 5342
# URL de la base de datos (ajusta con tu configuración de base de datos)
SQLALCHEMY_DATABASE_URL = "postgresql://odoo:odoo@localhost:5432/supermercado"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()

def get_db():
    db = SessionLocal()  # Crear una nueva sesión
    try:
        yield db  # Devuelve la sesión para su uso
    finally:
        db.close()  # Cierra la sesión después de usarla
