from sqlalchemy.orm import Session

from src.models.pedido import Pedido
from src.models.cliente import Cliente
from src.schemas.pedido import PedidoSchema, PedidoUpdate
from src.schemas.response import PedidoResponse

# Obtiene todos los pedidos
def obtener_pedidos(db: Session):

    pedidos = (
        db.query(Pedido.id_pedido, Cliente.nombre, Pedido.estado, Pedido.total)
        .join(Cliente, Pedido.id_cliente == Cliente.id_cliente)
        .all()
    )
    
    return [PedidoResponse(id_pedido=p.id_pedido, nombre=p.nombre, estado=p.estado, total=p.total) for p in pedidos]

# Obtiene un pedido por categoria
def obtener_pedido_por_id_de_cliente(id: int, db: Session):

    pedidos = (
        db.query(Pedido.id_pedido, Cliente.nombre, Pedido.estado, Pedido.total)
        .join(Cliente, Pedido.id_cliente == Cliente.id_cliente)
        .filter(Pedido.id_cliente == id)
        .all()
    )

    if not pedidos:
        raise Exception("Pedido no encontrado")
    
    return [PedidoResponse(id_pedido=p.id_pedido, nombre=p.nombre, estado=p.estado, total=p.total) for p in pedidos]

# Crea un pedido, se crea un pedido don id de cliente, estado = 'pendiente' y total en 0 
def crear_pedido(pedido: PedidoSchema, db: Session):
    nuevo_pedido = Pedido(id_cliente = pedido.id_cliente, estado = pedido.estado, 
                          total = pedido.total)
    db.add(nuevo_pedido)
    db.commit()
    db.refresh(nuevo_pedido)
    return {"message": "Pedido creado correctamente"}

# Actualiza pedido, se deberia actualizar con valores de pedido.estado 'en proceso' o 'enviado', el total se calcula en el front
def actualizar_pedido(id_pedido, id_cliente, pedido_data: PedidoUpdate, db: Session):

    # Buscar el pedido en la base de datos
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).filter(
        Pedido.id_cliente == id_cliente).first()
    
    if not pedido:
        raise Exception("Pedido no encontrado")

    # Actualizar solo los campos enviados
    for campo, valor in pedido_data.model_dump(exclude_unset=True).items():
        setattr(pedido, campo, valor)

    db.commit()  # Guardar cambios en la BD
    db.refresh(pedido)  # Refrescar datos del pedido
    return {"message": "Pedido actualizado correctamente"}
    
# Elimina un pedido
def eliminar_pedido(id_pedido, id_cliente, db: Session):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).filter(
        Pedido.id_cliente == id_cliente).first()

    if not pedido:
        raise Exception("Pedido no encontrado")
    
    db.delete(pedido)
    db.commit()
    
    return {"message": "Pedido eliminado correctamente"}