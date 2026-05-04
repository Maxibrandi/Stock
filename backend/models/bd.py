from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# --- Rol ---
class RolBase(BaseModel):
    nombre_rol: str = "Administrador"
    puede_ver_ganancias: bool = True

class Rol(RolBase):
    id: int

# --- Usuario ---
class UsuarioBase(BaseModel):
    nombre: str = "Admin_User"

class UsuarioCreate(UsuarioBase):
    contrasenia: str = "1234"

class Usuario(UsuarioBase):
    id: int
    rol: Rol

# --- Prenda ---
class PrendaBase(BaseModel):
    codigo_barras: str = "779123456789"
    talle: str = "xs", "s", "m", "l", "xl"
    tipo_tela: str = "Algodón"
    precio: float = 15000.0
    stock_minimo: int = 2

class PrendaCreate(PrendaBase):
    pass

class Prenda(PrendaBase):
    id: int
    stock_actual: int = 0

# --- Movimiento ---
class MovimientoBase(BaseModel):
    prenda_id: int
    tipo: str = "Entrada", "Salida"
    cantidad: int = 11

class MovimientoCreate(MovimientoBase):
    pass

class Movimiento(MovimientoBase):
    id: int
    fecha: datetime
    usuario_id: int

# --- Venta ---
class VentaBase(BaseModel):
    usuario_id: int

class VentaCreate(VentaBase):
    items: List[int]

class Venta(VentaBase):
    id: int
    fecha: datetime
    total: float