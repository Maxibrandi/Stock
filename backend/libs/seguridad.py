# /app/libs/seguridad.py
from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
import os
from models.bd import get_db, Usuario
from models.bd import Rol

# Configuración de encriptación y JWT
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("JWT_SECRET", "super-secreto-para-desarrollo-123456")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 360  # El token dura 6 horas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# --- FUNCIONES DE CONTRASEÑA ---
def hashear_contrasenia(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def verificar_contrasenia(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


# --- FUNCIONES DE JWT ---
def crear_token_acceso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# --- DEPENDENCIA PARA PROTEGER ENDPOINTS ---
def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception

    usuario = db.query(Usuario).filter(Usuario.nombre == username).first()
    if usuario is None:
        raise credentials_exception
    return usuario

# --- ROLES PARA VER VENTAS ---
def verificar_es_administrador(usuario_actual: Usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)) -> Usuario:
    """
    Verifica que el usuario tenga explícitamente el rol de Administrador.
    """
    rol = db.get(Rol, usuario_actual.rol_id)
    if not rol or rol.nombre_rol.lower() != "administrador":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Operación no permitida: Se requieren permisos de Administrador."
        )
    return usuario_actual

def verificar_permiso_ganancias(usuario_actual: Usuario = Depends(obtener_usuario_actual), db: Session = Depends(get_db)) -> Usuario:
    """
    Verifica si el rol del usuario tiene habilitado el permiso 'puede_ver_ganancias'.
    """
    rol = db.get(Rol, usuario_actual.rol_id)
    if not rol or not rol.puede_ver_ganancias:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso denegado: Tu rol no tiene permisos para ver información financiera."
        )
    return usuario_actual