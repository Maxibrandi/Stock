from pydantic import BaseModel, Field
from typing import Literal

# Estructura base compartida
class PrendaBase(BaseModel):
    nombre: str
    codigo_barras: str
    talle: Literal["xs", "s", "m", "l", "xl"]
    tipo_tela: str
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock_minimo: int = 2
    stock_actual: int = Field(gt=0, ge=0)

# Lo que se necesita para CREAR una prenda desde el frontend
class PrendaCreate(PrendaBase):
    pass

# Lo que la API de vuelve al frontend (incluye el ID y el stock)
class PrendaResponse(PrendaBase):
    id: int
    stock_actual: int

    class Config:
        from_attributes = True  # Le permite a Pydantic leer modelos de SQLAlchemy