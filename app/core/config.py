from pydantic_settings import BaseSettings
from datetime import datetime
from typing import Optional

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    PROJECT_NAME: str
    VERSION: str
    API_V1_STR: str
    
    # Base de datos
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_DB: str
    POSTGRES_URL: str
    
    # Seguridad
    JWT_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        case_sensitive = True
        env_file = ".env"

    @property
    def DATABASE_URL(self) -> str:
        """
        Obtiene la URL de la base de datos, usando POSTGRES_URL si está disponible,
        o construyéndola a partir de los componentes individuales.
        """
        if hasattr(self, 'POSTGRES_URL') and self.POSTGRES_URL:
            return self.POSTGRES_URL
            
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()