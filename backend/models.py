from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

# --- ENUMS PARA VALIDACIÓN SEMÁNTICA ---
class TalleEnum(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"


# --- ENTIDAD PRINCIPAL: PRENDA (Base y Tabla) ---
class PrendaBase(SQLModel):
    nombre: str = Field(index=True, max_length=100)
    codigo_barras: str = Field(unique=True, index=True, max_length=50)
    categoria: str = Field(index=True, max_length=50)  # Ej: "Remeras", "Pantalones"
    talle: TalleEnum
    tipo_tela: Optional[str] = Field(default=None, max_length=50) # Agregado desde tu PrendaModel
    precio: float = Field(default=0.0, gt=0)  # El precio debe ser mayor a 0
    stock_actual: int = Field(default=0, ge=0)  # El stock no puede ser negativo
    stock_minimo: int = Field(default=2, ge=0)  # Agregado desde tu PrendaModel


# Este modelo representa fielmente la tabla física en PostgreSQL
class Prenda(PrendaBase, table=True):
    __tablename__ = "prendas"

    id: Optional[int] = Field(default=None, primary_key=True)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)


# Esquemas de transferencia de datos (DTOs) específicos para la API
class PrendaCreate(PrendaBase):
    pass  # Datos requeridos para registrar una prenda nueva


class PrendaUpdate(SQLModel):
    nombre: Optional[str] = None
    codigo_barras: Optional[str] = None
    categoria: Optional[str] = None
    talle: Optional[TalleEnum] = None
    tipo_tela: Optional[str] = None
    precio: Optional[float] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None