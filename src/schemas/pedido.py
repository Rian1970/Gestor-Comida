from pydantic import BaseModel, Field, condecimal, field_validator
from typing import Optional, Annotated
from decimal import Decimal

# Crear un alias de tipo para precios decimales
DecimalType = Annotated[float, condecimal(max_digits=10, decimal_places=2, ge=0)] 

# Esquema Pydantic para crear
class PedidoSchema(BaseModel):
    id_cliente: int = Field(..., gt=0, example="1")
    estado: str = Field(..., min_length=2, max_length=50, example="Pendiente")
    total: DecimalType = Field(..., example="0.00")

# Esquema Pydantic para actualizar
class PedidoUpdate(BaseModel):
    estado: Optional[str] = None
    total: Optional[DecimalType] = None

    model_config = {
        'json_schema_extra' : {
            "example": {
                "estado": "En proceso",
                "total": "100.55"
            }
        }
    }

# Esquema Pydantic para el query de actualizacion y borrado
class PedidoQueryParams(BaseModel):
    id_pedido: int = Field(..., gt=0, example=1)
    id_cliente: int = Field(..., gt=0, example=1)