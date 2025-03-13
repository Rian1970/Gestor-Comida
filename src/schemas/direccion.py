from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional

# Esquema Pydantic para crear
class DireccionSchema(BaseModel):
    id_cliente: int = Field(..., gt=0, example="1")
    calle: str = Field(..., min_length=2, max_length=50, example="Dalia")
    colonia: str = Field(..., min_length=10, max_length=15, example="Santa Cruz")
    codigo_postal: int = Field(..., gt=0, example="09292")
    numero: int = Field(..., gt=0, example="154")
    referencias: str = Field(..., min_length=0, max_length=255, example="Calle cerrada")

# Esquema Pydantic para actualizar
class DireccionUpdate(BaseModel):
    calle: Optional[str] = None
    colonia: Optional[str] = None
    codigo_postal: Optional[str] = None
    numero: Optional[int] = None
    referencias: Optional[str] = None

    model_config = {
        'json_schema_extra' : {
            "example": {
                "calle": "Dalia",
                "colonia": "Santa Cruz",
                "codigo_postal": "09292",
                "numero": "154",
                "referencias": "Calle cerrada"
            }
        }
    }

# Esquema Pydantic para el query de actualizacion y borrado
class DireccionQueryParams(BaseModel):
    id_direccion: int = Field(..., gt=0, example=1)
    id_cliente: int = Field(..., gt=0, example=1)