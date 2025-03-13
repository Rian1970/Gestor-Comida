from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Direccion(Base):
    __tablename__ = "direccion"

    id_direccion = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente", ondelete="CASCADE"), nullable=False)
    calle = Column(String(50), nullable=False)
    colonia = Column(String(50), nullable=False)
    codigo_postal = Column(Integer, nullable=False)
    numero = Column(Integer, nullable=False)
    referencias = Column(String(255))

    # Relación con Cliente
    cliente = relationship("Cliente", backref="direcciones")
