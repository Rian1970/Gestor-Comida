from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.detalle_pedido import DetallePedidoSchema, DetallePedidoUpdate, DetallePedidoQueryParams
from src.services.detalle_pedido_service import (
    obtener_detalle_pedidos,
    obtener_detalle_pedido_por_id,
    crear_detalle_pedido,
    actualizar_detalle_pedido,
    eliminar_detalle_pedido
)

detalle_pedido_router = APIRouter()

# Obtener todos los detalle_pedidos
@detalle_pedido_router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Detalle_pedidos'],
    responses={
        200: {"description": "OK"}
    }
)
def get_detalle_pedidos(db: Session = Depends(get_db)):
   
    return obtener_detalle_pedidos(db)

# Obtener detalle_pedido por id
@detalle_pedido_router.get(
    "/por_id_pedido_y_cliente", 
    status_code=status.HTTP_200_OK, 
    tags=['Detalle_pedidos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "El pedido no existe"}
    }
)
def get_detalle_pedido_por_id(id_pedido: int = Query(gt = 0), id_cliente: int = Query(gt = 0), db: Session = Depends(get_db)):
    
    return obtener_detalle_pedido_por_id(id_pedido, id_cliente, db)

# Crear un detalle_pedido nuevo
@detalle_pedido_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    tags=['Detalle_pedidos'],
    responses={
        201: {"description": "Detalle del pedido creado exitosamente"},
        404: {"description": "Pedido no creado"},
        500: {"description": "Error del servidor"}
    }
)
def create_detalle_pedido(detalle_pedido: DetallePedidoSchema, id_cliente: int = Query(gt = 0), db: Session = Depends(get_db)):
    try:
        return crear_detalle_pedido(detalle_pedido, id_cliente, db)
    except Exception as e:
            if "Pedido no creado" in str(e):
                raise HTTPException(status_code=404, detail=str(e))
            raise HTTPException(status_code=500, detail="Error del servidor")

# Actualizar un detalle_pedido
@detalle_pedido_router.put(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Detalle_pedidos'],
    responses={
        200: {"description": "Detalle del pedido actualizado exitosamente"},
        404: {"description": "Detalle del pedido no encontrado"},
        500: {"description": "Error del servidor"}
    }
)
def update_pedido(
    params: DetallePedidoQueryParams,  
    detalle_pedido_data: DetallePedidoUpdate,  # Datos de entrada validados
    db: Session = Depends(get_db)
):
    try:
        return actualizar_detalle_pedido(params.id_pedido, params.id_producto, detalle_pedido_data, db)
    except Exception as e:
        if "Detalle del pedido no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")

# Eliminar un detalle_pedido
@detalle_pedido_router.delete(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Detalle_pedidos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "detalle_pedido no encontrado"}
    }
)
def delete_detalle_pedido(params: DetallePedidoQueryParams, db: Session = Depends(get_db)):

    try:
        return eliminar_detalle_pedido(params.id_pedido, params.id_producto, db)
    except Exception as e:
        if "Detalle del pedido no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")