from sqlalchemy.orm import Session

from src.models.detalle_pedido import DetallePedido
from src.models.cliente import Cliente
from src.models.pedido import Pedido
from src.models.producto import Producto
from src.schemas.detalle_pedido import DetallePedidoSchema, DetallePedidoUpdate
from src.schemas.response import DetallePedidoResponse

# Obtiene todos los detalles de pedidos
def obtener_detalle_pedidos(db: Session):

    detalle_pedidos = (
        db.query(DetallePedido.id_pedido, Cliente.nombre.label("nombre_cliente"), DetallePedido.cantidad, 
                 Producto.nombre.label("nombre_producto"), DetallePedido.subtotal)
        .join(Pedido, Pedido.id_pedido == DetallePedido.id_pedido)
        .join(Producto, Producto.id_producto == DetallePedido.id_producto)
        .join(Cliente, Cliente.id_cliente == Pedido.id_cliente)
        .all()
    )

    return [DetallePedidoResponse(id_pedido=p.id_pedido, nombre_cliente=p.nombre_cliente, 
                           cantidad=p.cantidad, nombre_producto=p.nombre_producto, 
                           subtotal=p.subtotal) for p in detalle_pedidos]

# Obtiene un detalle pedido por id 
def obtener_detalle_pedido_por_id(id_pedido: int, id_cliente: int, db: Session):

    # Consulta principal
    detalle_pedidos = (
        db.query(
            DetallePedido.id_pedido, 
            Cliente.nombre.label("nombre_cliente"), 
            DetallePedido.cantidad, 
            Producto.nombre.label("nombre_producto"), 
            DetallePedido.subtotal, 
        )
        .join(Pedido, Pedido.id_pedido == DetallePedido.id_pedido)
        .join(Producto, Producto.id_producto == DetallePedido.id_producto)
        .join(Cliente, Cliente.id_cliente == Pedido.id_cliente)
        .filter(Pedido.id_pedido == id_pedido)  
        .filter(Pedido.id_cliente == id_cliente)  
        .all()
    )

    # Convertir resultados en lista de respuestas
    return [
        DetallePedidoResponse(
            id_pedido=p.id_pedido, 
            nombre_cliente=p.nombre_cliente, 
            cantidad=p.cantidad, 
            nombre_producto=p.nombre_producto, 
            subtotal=p.subtotal
        ) 
        for p in detalle_pedidos
    ]


# Crea un detalle_pedido 
def crear_detalle_pedido(detalle_pedido: DetallePedidoSchema, id_cliente: int, db: Session):

    pedido = (
        db.query(Pedido)
        .filter(Pedido.id_cliente == id_cliente)
        .filter(Pedido.estado == 'Pendiente')
        .first()
    )

    if not pedido:
        raise Exception("Pedido no creado")

    nuevo_detalle_pedido = DetallePedido(id_pedido = pedido.id_pedido, 
                            id_producto = detalle_pedido.id_producto, cantidad = detalle_pedido.cantidad, 
                            subtotal = detalle_pedido.subtotal)
    
    db.add(nuevo_detalle_pedido)
    db.commit()
    db.refresh(nuevo_detalle_pedido)
    return {"message": "Detalle del pedido creado correctamente"}

#  Actualiza detalle_pedido
def actualizar_detalle_pedido(id_pedido, id_producto, detalle_pedido_data: DetallePedidoUpdate, db: Session):
    # Buscar el detalle del pedido en la base de datos
    detalle_pedido = db.query(DetallePedido).filter(DetallePedido.id_pedido == id_pedido).filter(
        DetallePedido.id_producto == id_producto).first()
    
    if not detalle_pedido:
        raise Exception("Detalle del pedido no encontrado")

    # Actualizar solo los campos enviados
    for campo, valor in detalle_pedido_data.model_dump(exclude_unset=True).items():
        setattr(detalle_pedido, campo, valor)

    db.commit()  # Guardar cambios en la BD
    db.refresh(detalle_pedido)  # Refrescar datos del pedido
    return {"message": "Detalle del pedido actualizado correctamente"}
    
# Elimina un detalle_pedido
def eliminar_detalle_pedido(id_pedido, id_producto, db: Session):
    detalle_pedido = (db.query(DetallePedido).filter(DetallePedido.id_pedido == id_pedido)
                      .filter(DetallePedido.id_producto == id_producto).first())

    if not detalle_pedido:
        raise Exception("Detalle del pedido no encontrado")
    
    db.delete(detalle_pedido)
    db.commit()
    
    return {"message": "Detalle pedido eliminado correctamente"}