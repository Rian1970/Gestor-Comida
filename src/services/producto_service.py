from sqlalchemy.orm import Session

from src.models.producto import Producto
from src.schemas.producto import ProductoSchema, ProductoUpdate

# Obtiene todos los productos
def obtener_productos(db: Session):

    return db.query(Producto).all()

# Obtiene un producto por categoria
def obtener_producto_por_categoria(categoria: str, db: Session):
       
    return db.query(Producto).filter(Producto.categoria == categoria).all()

# Crea un producto 
def crear_producto(producto: ProductoSchema, db: Session):
    nuevo_producto = Producto(nombre=producto.nombre, descripcion=producto.descripcion, 
                              precio=producto.precio, categoria=producto.categoria)
    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return {"message": "Producto creado correctamente"}

# Actualiza producto
def actualizar_producto(id_producto: int, producto_data: ProductoUpdate, db: Session):

    # Buscar el producto en la base de datos
    producto = db.query(Producto).filter(Producto.id_producto == id_producto).first()
    
    if not producto:
        raise Exception("Producto no encontrado")

    # Actualizar solo los campos enviados
    for campo, valor in producto_data.model_dump(exclude_unset=True).items():
        setattr(producto, campo, valor)

    db.commit()  # Guardar cambios en la BD
    db.refresh(producto)  # Refrescar datos del producto
    return {"message": "Producto actualizado correctamente"}
    
# Elimina un producto
def eliminar_producto(id: int, db: Session):
    producto = db.query(Producto).filter(Producto.id_producto == id).first()

    if not producto:
        raise Exception("Producto no encontrado")
    
    db.delete(producto)
    db.commit()
    
    return {"message": "Producto eliminado correctamente"}