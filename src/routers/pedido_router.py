from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.pedido import PedidoSchema, PedidoUpdate, PedidoQueryParams
from src.services.pedido_service import (
    obtener_pedidos,
    obtener_pedido_por_id_de_cliente,
    crear_pedido,
    actualizar_pedido,
    eliminar_pedido
)

pedido_router = APIRouter()

# Obtener todos los pedidos
@pedido_router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Pedidos'],
    responses={
        200: {"description": "OK"}
    }
)
def get_pedidos(db: Session = Depends(get_db)):
   
    return obtener_pedidos(db)

# Obtener pedido por id de cliente
@pedido_router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Pedidos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "Pedido no encontrado"}
    }
)
def get_pedidos_por_id_de_cliente(id: int = Path(gt=0), db: Session = Depends(get_db)):
    
    try:
        return obtener_pedido_por_id_de_cliente(id, db)
    except Exception as e:
        if "Pedido no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")

# Crear un pedido nuevo
@pedido_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    tags=['Pedidos'],
    responses={
        201: {"description": "Pedido creado exitosamente"}
    }
)
def create_pedido(pedido: PedidoSchema, db: Session = Depends(get_db)):

    return crear_pedido(pedido, db)

# Actualizar un pedido
@pedido_router.put(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Pedidos'],
    responses={
        200: {"description": "Pedido actualizado exitosamente"},
        404: {"description": "Pedido no encontrado"},
        500: {"description": "Error del servidor"}
    }
)
def update_pedido(
    params: PedidoQueryParams,  
    pedido_data: PedidoUpdate,  # Datos de entrada validados
    db: Session = Depends(get_db)
):
    try:
        return actualizar_pedido(params.id_pedido, params.id_cliente, pedido_data, db)
    except Exception as e:
        if "Pedido no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")
    
# Eliminar un pedido
@pedido_router.delete(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Pedidos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "Pedido no encontrado"}
    }
)
def delete_pedido(params: PedidoQueryParams, db: Session = Depends(get_db)):

    try:
        return eliminar_pedido(params.id_pedido, params.id_cliente, db)
    except Exception as e:
        if "Pedido no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")