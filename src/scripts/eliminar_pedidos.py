from sqlalchemy.orm import Session
from src.database import SessionLocal
from sqlalchemy import text

def eliminar_pedidos_expirados():
    """Elimina pedidos que tengan más de 7 días."""
    db: Session = SessionLocal()
    try:
        estado = 'Pendiente'
        resultado = db.execute(text("DELETE FROM pedido WHERE estado = :estado"), {"estado": estado})
        db.commit()
        print(f"Pedidos eliminados: {resultado.rowcount}")
    except Exception as e:
        print(f"Error al eliminar pedidos: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Ejecutando limpieza de pedidos expirados...")
    eliminar_pedidos_expirados()
    print("Limpieza completada.")
