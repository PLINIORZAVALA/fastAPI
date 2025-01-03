"""
Este módulo define los modelos de datos utilizados en la base de datos.
Incluye tablas y columnas definidas con SQLAlchemy.
"""

from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from database import Base

Base = declarative_base()

# Modelo de la tabla 'items'
class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)

