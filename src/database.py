from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.config import ConfigMySQL, ConfigPSQL  # Importar configuración

# Configurar la conexión a MySQL usando SQLAlchemy
DATABASE_URL = f"postgresql://{ConfigPSQL.PSQL_USER}:{ConfigPSQL.PSQL_PASSWORD}@{ConfigPSQL.PSQL_HOST}/{ConfigPSQL.PSQL_DB}"
# DATABASE_URL = f"mysql+pymysql://{ConfigMySQL.MYSQL_USER}:{ConfigMySQL.MYSQL_PASSWORD}@{ConfigMySQL.MYSQL_HOST}/{ConfigMySQL.MYSQL_DB}"

#Conecta a la base de datos y las consultas se habilitan para ver en consola
engine = create_engine(DATABASE_URL, echo=True)

# Crear una sesión basada en la conexion anteior para interactuar con la base de datos, 
# las banderas de para guardar y autorefrescar estan deshabilitadas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base para los modelos, aqui es donde se crea el objeto para mapear los registros de la BD a objetos en PY
Base = declarative_base()

# Dependencia para obtener la sesión en rutas
def get_db():
    db = SessionLocal()
    try:
        yield db  # Devuelve la sesión para su uso en rutas
    finally:
        db.close()  # Cierra la conexión después de la petición
