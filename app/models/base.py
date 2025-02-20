from sqlalchemy.orm import declarative_base
from datetime import datetime
from sqlalchemy import Column, Integer, DateTime

Base = declarative_base()

class BaseModel(Base):
    """Modelo base con campos comunes"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)