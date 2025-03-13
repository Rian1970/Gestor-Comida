from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from src.database import Base

class DetallePedido(Base):
    __tablename__ = "detalle_pedido"

    id_pedido = Column(Integer, ForeignKey("pedido.id_pedido", ondelete="CASCADE"), primary_key=True)
    id_producto = Column(Integer, ForeignKey("producto.id_producto", ondelete="CASCADE"), primary_key=True)
    cantidad = Column(Integer, nullable=False)
    subtotal = Column(DECIMAL(10,2), nullable=False)
