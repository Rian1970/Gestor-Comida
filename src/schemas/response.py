from pydantic import BaseModel

class PedidoResponse(BaseModel):
    id_pedido: int
    nombre: str
    estado: str
    total: float

class DetallePedidoResponse(BaseModel):
    id_pedido: int
    nombre_cliente: str
    cantidad: int
    nombre_producto: str
    subtotal: float