from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="API para gestión de biblioteca digital",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configuración CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir los routers de la API
app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    """
    Endpoint raíz que proporciona información básica de la API.
    """
    return {
        "message": "Bienvenido a la API de Biblioteca Digital",
        "version": settings.VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }