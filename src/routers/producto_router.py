from fastapi import Depends, APIRouter, HTTPException, Path, Query, status
from sqlalchemy.orm import Session

from src.database import get_db
from src.schemas.producto import ProductoSchema, ProductoUpdate
from src.services.producto_service import (
    obtener_productos,
    obtener_producto_por_categoria,
    crear_producto,
    actualizar_producto,
    eliminar_producto
)

producto_router = APIRouter()

# Obtener todos los productos
@producto_router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    tags=['Productos'],
    responses={
        200: {"description": "OK"}
    }
)
def get_productos(db: Session = Depends(get_db)):
   
    return obtener_productos(db)

# Obtener producto por categoria
@producto_router.get(
    "/por_categoria", 
    status_code=status.HTTP_200_OK, 
    tags=['Productos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "La categoria no existe"}
    }
)
def get_productos_por_categoria(categoria: str = Query(min_length=2, max_length=50), db: Session = Depends(get_db)):
    
    return obtener_producto_por_categoria(categoria, db)

# Crear un producto nuevo
@producto_router.post(
    "/", 
    status_code=status.HTTP_201_CREATED, 
    tags=['Productos'],
    responses={
        201: {"description": "Producto creado exitosamente"}
    }
)
def create_producto(producto: ProductoSchema, db: Session = Depends(get_db)):

    return crear_producto(producto, db)

# Actualizar un producto
@producto_router.put(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Productos'],
    responses={
        200: {"description": "producto actualizado exitosamente"},
        404: {"description": "Producto no encontrado"},
        500: {"description": "Error del servidor"}
    }
)
def update_producto(
    id_producto: int,
    producto_data: ProductoUpdate,  # Datos de entrada validados
    db: Session = Depends(get_db)
):
    try:
        return actualizar_producto(id_producto, producto_data, db)
    except Exception as e:
        if "Producto no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")

# Eliminar un producto
@producto_router.delete(
    "/{id}", 
    status_code=status.HTTP_200_OK, 
    tags=['Productos'],
    responses={
        200: {"description": "OK"},
        404: {"description": "Producto no encontrado"}
    }
)
def delete_producto(id: int = Path(gt = 0), db: Session = Depends(get_db)):

    try:
        return eliminar_producto(id, db)
    except Exception as e:
        if "Producto no encontrado" in str(e):
            raise HTTPException(status_code=404, detail=str(e))
        raise HTTPException(status_code=500, detail="Error del servidor")