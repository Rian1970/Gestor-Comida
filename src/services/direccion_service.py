from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.direccion import Direccion
from src.schemas.direccion import DireccionSchema, DireccionUpdate

# Obtiene todos los direcciones
def obtener_direcciones(db: Session):

    return db.query(Direccion).all()

# Obtiene un direccion por id de usuario
def obtener_direccion_por_id_de_usuario(id: int, db: Session):
    
    return db.query(Direccion).filter(Direccion.id_cliente == id).all()

# Crea una direccion 
def crear_direccion(direccion: DireccionSchema, db: Session):
    nueva_direccion = Direccion(id_cliente = direccion.id_cliente, calle = direccion.calle,
                                colonia = direccion.colonia, codigo_postal = direccion.codigo_postal,
                                numero = direccion.numero, referencias = direccion.referencias)
    db.add(nueva_direccion)
    db.commit()
    db.refresh(nueva_direccion)
    return {"message": "Direccion creada correctamente"}

# Actualiza direccion
def actualizar_direccion(id_direccion: int, id_cliente: int, direccion_data: DireccionUpdate, db: Session):

    # Buscar el direccion en la base de datos
    direccion = db.query(Direccion).filter(Direccion.id_direccion == id_direccion).filter(
            Direccion.id_cliente == id_cliente).first()
    
    if not direccion:
        raise Exception("Direccion no encontrada")

    # Actualizar solo los campos enviados
    for campo, valor in direccion_data.model_dump(exclude_unset=True).items():
        setattr(direccion, campo, valor)

    db.commit()  # Guardar cambios en la BD
    db.refresh(direccion)  # Refrescar datos de la direccion
    return {"message": "Direccion actualizada correctamente"}

# Elimina un direccion
def eliminar_direccion(id_direccion: int, id_cliente: int, db: Session):
    direccion = db.query(Direccion).filter(Direccion.id_direccion == id_direccion).filter(
            Direccion.id_cliente == id_cliente).first()

    if not direccion:
        raise Exception("Direccion no encontrada")
    
    db.delete(direccion)
    db.commit()
    
    return {"message": "Direccion eliminada correctamente"}