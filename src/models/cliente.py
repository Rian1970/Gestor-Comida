from sqlalchemy import Column, Integer, String
from src.database import Base

# Modelo SQLAlchemy
class Cliente(Base):
    __tablename__ = "cliente"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    telefono = Column(String(50), nullable=False)
    correo = Column(String(50), unique=True, nullable=False)
    contrasenia = Column(String(50), nullable=False)
