from pydantic import BaseModel, Field, condecimal, field_validator
from typing import Optional, Annotated
from decimal import Decimal

# Crear un alias de tipo para precios decimales
DecimalType = Annotated[float, condecimal(max_digits=10, decimal_places=2, ge=0)] 

# Esquema Pydantic para crear
class DetallePedidoSchema(BaseModel):
    id_producto: int = Field(..., gt=0, example="1")
    cantidad: int = Field(..., gt=0, example="1")
    subtotal: DecimalType = Field(..., example="150.00")

# Esquema Pydantic para actualizar
class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int] = None
    subtotal: Optional[DecimalType] = None

    model_config = {
        'json_schema_extra' : {
            "example": {
                "cantidad": "3",
                "subtotal": "90.00"
            }
        }
    }

# Esquema Pydantic para el query de actualizacion y borrado
class DetallePedidoQueryParams(BaseModel):
    id_pedido: int = Field(..., gt=0, example=1)
    id_producto: int = Field(..., gt=0, example=1)