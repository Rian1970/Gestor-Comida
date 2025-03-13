from fastapi import Depends, APIRouter, HTTPException, Path, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.cliente import ClienteSchema, ClienteUpdate
from src.services.cliente_service import (
    obtener_clientes, 
    obtener_cliente_por_id, 
    crear_cliente, 
    actualizar_cliente, 
    eliminar_cliente
)

cliente_router = APIRouter()

# Obtener todos los clientes
@cliente_router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Clientes'],
    responses={
        200: {"description": "OK"}
    }
)
def get_clientes(db: Session = Depends(get_db)):

    return obtener_clientes(db)

# Obtener cliente por id
@cliente_router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Clientes'],
    responses={
        200: {"description": "OK"},
        404: {"description": "El cliente no existe"}
    }
)
def get_cliente_por_id(id: int = Path(gt = 0), db: Session = Depends(get_db)):
    
    cliente = obtener_cliente_por_id(id, db)

    if not cliente:
            raise HTTPException(status_code=404, detail="El cliente no existe")

    return cliente

# Crear un cliente nuevo
@cliente_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    tags=['Clientes'],
    responses={
        201: {"description": "Cliente creado exitosamente"},
        409: {"description": "El correo ya está registrado"},
        500: {"description": "Error del servidor"}
    }
)
def create_cliente(cliente: ClienteSchema, db: Session = Depends(get_db)):
    
    try:
        return crear_cliente(cliente, db)
    except Exception as e:
        if "El correo ya esta registrado" in str(e):
            raise HTTPException(status_code=409, detail="El correo ya esta registrado")
        
        raise HTTPException(status_code=500, detail="Error del servidor")

# Actualizar un cliente
@cliente_router.put(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Clientes'],
    responses={
        200: {"description": "Cliente actualizado exitosamente"},
        404: {"description": "El cliente no existe"},
        409: {"description": "El correo ya está registrado"},
        500: {"description": "Error del servidor"}
    }
)
def update_cliente(
    id_cliente: int,
    cliente_data: ClienteUpdate,  # Datos de entrada validados
    db: Session = Depends(get_db)
):
    try:
        return actualizar_cliente(id_cliente, cliente_data, db)
    except Exception as e:
        if "El cliente no existe" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        
        if "El correo ya esta registrado" in str(e):
            raise HTTPException(status_code=409, detail=str(e))
        
        raise HTTPException(status_code=500, detail="Error del servidor")
    
# Eliminar un cliente
@cliente_router.delete(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Clientes'],
    responses={
        200: {"description": "OK"},
        404: {"description": "El cliente no existe"}
    }
)
def delete_cliente(id: int = Path(gt = 0), db: Session = Depends(get_db)):
    
    try:
        return eliminar_cliente(id, db)
    except Exception as e:
        if "El cliente no existe" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
            
        raise HTTPException(status_code=500, detail="Error del servidor")