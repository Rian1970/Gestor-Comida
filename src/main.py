from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.cliente_router import cliente_router
from src.routers.producto_router import producto_router
from src.routers.direccion_router import direccion_router
from src.routers.pedido_router import pedido_router
from src.routers.detalle_pedido_router import detalle_pedido_router

app = FastAPI()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite solicitudes de todos los orígenes (cambia a tus dominios específicos en producción)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos HTTP (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)

app.include_router(prefix='/clientes', router=cliente_router)
app.include_router(prefix='/productos', router=producto_router)
app.include_router(prefix='/direcciones', router=direccion_router)
app.include_router(prefix='/pedidos', router=pedido_router)
app.include_router(prefix='/detalle_pedidos', router=detalle_pedido_router)



