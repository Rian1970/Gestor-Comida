from sqlalchemy import Column, Integer, String, DECIMAL
from src.database import Base

# Modelo SQLAlchemy
class Producto(Base):
    __tablename__ = "producto"

    id_producto = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(String(255))
    precio = Column(DECIMAL(10,2), nullable=False)
    categoria = Column(String(50), nullable=False)
