from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from src.database import Base

class Pedido(Base):
    __tablename__ = "pedido"

    id_pedido = Column(Integer, primary_key=True, autoincrement=True)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente", ondelete="CASCADE"), nullable=False)
    estado = Column(String(50), nullable=False)
    total = Column(DECIMAL(10,2), nullable=True)

    # Relación con Cliente
    cliente = relationship("Cliente", backref="pedidos")
