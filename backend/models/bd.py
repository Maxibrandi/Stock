from typing import Optional, List
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship, create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/stock_db")
engine = create_engine(DATABASE_URL, echo=True)


def get_db():
    with Session(engine) as session:
        yield session


# --- ENUMS ---
class TalleEnum(str, Enum):
    xs = "xs"
    s = "s"
    m = "m"
    l = "l"
    xl = "xl"


class TipoMovimientoEnum(str, Enum):
    entrada = "Entrada"
    salida = "Salida"


# --- MODELOS DE ROLES Y USUARIOS ---
class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_rol: str = Field(default="Administrador", unique=True, max_length=50)
    puede_ver_ganancias: bool = Field(default=True)
    usuarios: List["Usuario"] = Relationship(back_populates="rol")


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(index=True, unique=True, max_length=50)
    contrasenia: str = Field(max_length=255)
    rol_id: int = Field(foreign_key="roles.id")
    rol: Optional[Rol] = Relationship(back_populates="usuarios")


# --- MODELOS PARA PRENDAS ---
class PrendaBase(SQLModel):
    nombre: str = Field(default="Remera Oversize Negra", max_length=100)
    codigo_barras: Optional[str] = Field(default="779123456789", unique=True, index=True, max_length=50)
    categoria: str = Field(default="Remeras", index=True, max_length=50)
    talle: TalleEnum
    tipo_tela: Optional[str] = Field(default="Algodón", max_length=50)
    stock_minimo: int = Field(default=2, ge=0)
    stock_actual: int = Field(default=0, ge=0)
    precio: float = Field(default=15000.0, gt=0)


class Prenda(PrendaBase, table=True):
    __tablename__ = "prendas"
    id: Optional[int] = Field(default=None, primary_key=True)

    def verificar_alerta_stock(self) -> bool:
        if self.stock_actual <= self.stock_minimo:
            print(f"ALERTA: Stock mínimo para {self.tipo_tela} (Talle {self.talle})")
            return True
        return False


class PrendaCreate(PrendaBase):
    pass


class PrendaUpdate(SQLModel):
    nombre: Optional[str] = None
    codigo_barras: Optional[str] = None
    talle: Optional[TalleEnum] = None
    tipo_tela: Optional[str] = None
    precio: Optional[float] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None


# --- MODELOS PARA MOVIMIENTOS ---
class MovimientoBase(SQLModel):
    prenda_id: int = Field(foreign_key="prendas.id", index=True)
    usuario_id: int = Field(foreign_key="usuarios.id")
    tipo: TipoMovimientoEnum = Field(index=True)
    cantidad: int = Field(default=1, gt=0)
    fecha: datetime = Field(default_factory=datetime.utcnow)


class Movimiento(MovimientoBase, table=True):
    __tablename__ = "movimientos"
    id: Optional[int] = Field(default=None, primary_key=True)


class MovimientoCreate(SQLModel):
    prenda_id: int
    tipo: TipoMovimientoEnum
    cantidad: int


# --- MODELOS PARA VENTAS (Estructura Relacional Unificada) ---
class DetalleVenta(SQLModel, table=True):
    __tablename__ = "detalles_ventas"
    id: Optional[int] = Field(default=None, primary_key=True)
    venta_id: Optional[int] = Field(default=None, foreign_key="ventas.id", index=True)
    prenda_id: int = Field(foreign_key="prendas.id")
    cantidad: int = Field(default=1, gt=0)
    precio_unitario: float = Field(gt=0)


class VentaBase(SQLModel):
    usuario_id: int = Field(foreign_key="usuarios.id")
    fecha: datetime = Field(default_factory=datetime.utcnow)
    total: float = Field(default=0.0, ge=0)


class Venta(VentaBase, table=True):
    __tablename__ = "ventas"
    id: Optional[int] = Field(default=None, primary_key=True)


# --- ESQUEMAS DE VALIDACIÓN DE VENTAS ---
class ItemVentaCreate(SQLModel):
    prenda_id: int
    cantidad: int = 1


class VentaCreate(SQLModel):
    usuario_id: int
    items: List[ItemVentaCreate]


# --- REBUILD ---
Rol.model_rebuild()
Usuario.model_rebuild()