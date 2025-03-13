from pydantic import BaseModel, Field, condecimal, field_validator
from typing import Optional, Annotated
from decimal import Decimal

# Crear un alias de tipo para precios decimales
DecimalType = Annotated[float, condecimal(max_digits=10, decimal_places=2, ge=0)] 

# Esquema Pydantic para crear
class ProductoSchema(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, example="Pizza Mexicana")
    descripcion: str = Field(..., min_length=10, max_length=255, example="Una pizza con aguacate y frijoles")
    precio: DecimalType = Field(..., example="190.55")
    categoria: str = Field(..., min_length=2, max_length=50, example="Pizzas")

# Esquema Pydantic para actualizar
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[DecimalType] = None
    categoria: Optional[str] = None

    model_config = {
        'json_schema_extra' : {
            "example": {
                "nombre": "Pizza Mexicana",
                "descripcion": "Una pizza con aguacate y frijoles",
                "precio": "190.55",
                "categoria": "Pizzas"
            }
        }
    }