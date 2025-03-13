from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.direccion import DireccionSchema, DireccionUpdate, DireccionQueryParams
from src.services.direccion_service import (
    obtener_direcciones,
    obtener_direccion_por_id_de_usuario,
    crear_direccion,
    actualizar_direccion,
    eliminar_direccion
)

direccion_router = APIRouter()

# Obtener todos las direcciones
@direccion_router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Direcciones'],
    responses={
        200: {"description": "OK"}
    }
)
def get_direcciones(db: Session = Depends(get_db)):
   
    return obtener_direcciones(db)

# Obtener direccion por id de usuario
@direccion_router.get(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Direcciones'],
    responses={
        200: {"description": "OK"},
        404: {"description": "El cliente no existe"}
    }
)
def get_direcciones_por_id_de_usuario(id: int = Path(gt=0), db: Session = Depends(get_db)):
    
    return obtener_direccion_por_id_de_usuario(id, db)

# Crear una direccion nueva
@direccion_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    tags=['Direcciones'],
    responses={
        201: {"description": "Direccion creada exitosamente"}
    }
)
def create_direccion(direccion: DireccionSchema, db: Session = Depends(get_db)):

    return crear_direccion(direccion, db)

# Actualizar un direccion
@direccion_router.put(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Direcciones'],
    responses={
        200: {"description": "Direccion actualizada exitosamente"},
        404: {"description": "Direccion no encontrada"},
        500: {"description": "Error del servidor"}
    }
)
def update_direccion(
    params: DireccionQueryParams,  
    direccion_data: DireccionUpdate,  # Datos de entrada validados
    db: Session = Depends(get_db)
):
    try:
        return actualizar_direccion(params.id_direccion, params.id_cliente, direccion_data, db)
    except Exception as e:
        if "Direccion no encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")
    
# Eliminar un direccion
@direccion_router.delete(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Direcciones'],
    responses={
        200: {"description": "OK"},
        404: {"description": "Direccion no encontrada"}
    }
)
def delete_direccion(params: DireccionQueryParams, db: Session = Depends(get_db)):

    try:
        return eliminar_direccion(params.id_direccion, params.id_cliente, db)
    except Exception as e:
        if "Direccion no encontrada" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")