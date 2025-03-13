from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.cliente import Cliente
from src.schemas.cliente import ClienteSchema, ClienteUpdate

# Obtiene todos los clientes
def obtener_clientes(db: Session):

    return db.query(Cliente).all()

# Obtiene un cliente por id
def obtener_cliente_por_id(id: int, db: Session):
    
    return db.query(Cliente).filter(Cliente.id_cliente == id).first()

# Crea un cliente 
def crear_cliente(cliente: ClienteSchema, db: Session):
    nuevo_cliente = Cliente(nombre=cliente.nombre, telefono=cliente.telefono, correo=cliente.correo,
                             contrasenia=cliente.contrasenia)
    try:
        db.add(nuevo_cliente)
        db.commit()
        db.refresh(nuevo_cliente)
        return {"message": "Cliente creado correctamente"}
    
    except IntegrityError:  # Si el correo ya existe (por restricción UNIQUE)
        db.rollback()  # Revierte la transacción para evitar errores en la BD
        raise Exception("El correo ya esta registrado")
    
    except Exception as e:  # Manejo de otros errores inesperados
        db.rollback()
        raise Exception(str(e))

# Actualiza cliente
def actualizar_cliente(id_cliente: int, cliente_data: ClienteUpdate, db: Session):

    # Buscar el cliente en la base de datos
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()
    
    if not cliente:
        raise Exception("El cliente no exist")

    # Actualizar solo los campos enviados
    for campo, valor in cliente_data.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)

    try:
        db.commit()  # Guardar cambios en la BD
        db.refresh(cliente)  # Refrescar datos del cliente
        return {"message": "Cliente actualizado correctamente"}
    
    except IntegrityError:  # Si el correo ya existe (por restricción UNIQUE)
        db.rollback()  # Revierte la transacción para evitar errores en la BD
        raise Exception("El correo ya esta registrado")
    
    except Exception as e:  # Manejo de otros errores inesperados
        db.rollback()
        raise Exception(str(e))
    
# Elimina un cliente
def eliminar_cliente(id: int, db: Session):
    cliente = db.query(Cliente).filter(Cliente.id_cliente == id).first()

    if not cliente:
        raise Exception("El cliente no existe")
    
    db.delete(cliente)
    db.commit()
    
    return {"message": "Cliente eliminado correctamente"}