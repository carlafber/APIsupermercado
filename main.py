from fastapi import FastAPI, Request
import uvicorn
from app import models
from app.routers import user, producto, categoria, lista_compra, supermercado
from app.db.iniciar_db import *
from app.db.database import *
from fastapi.responses import JSONResponse
from app.exceptions import NotFoundException, UnauthorizedException, ForbiddenException, BadRequestException, InternalServerErrorException



def create_tables():
    try:
        Base.metadata.create_all(bind=engine)
        print("Tablas creadas con éxito.")
    except Exception as e:
        print(f"Error al crear las tablas: {e}")

create_tables()

app = FastAPI(
    title="API de Supermercados",  # Título de la API
    description="API para gestionar productos, supermercados, categorías y listas de compra.",
)

# Manejo global de excepciones
@app.exception_handler(NotFoundException)
async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(UnauthorizedException)
async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(ForbiddenException)
async def forbidden_exception_handler(request: Request, exc: ForbiddenException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(BadRequestException)
async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

@app.exception_handler(InternalServerErrorException)
async def internal_server_error_exception_handler(request: Request, exc: InternalServerErrorException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

# Captura cualquier otra excepción (500 Internal Server Error)
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Error interno del servidor. Intenta más tarde."}
    )


# Llamar a la función cuando la aplicación inicie
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    cargar_bd(db)
    db.close()

app.include_router(user.router)
app.include_router(supermercado.router)
app.include_router(categoria.router)
app.include_router(producto.router)
app.include_router(lista_compra.router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
