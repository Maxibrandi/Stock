# /app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from models.bd import get_db, Usuario, Rol
from libs.seguridad import hashear_contrasenia, verificar_contrasenia, crear_token_acceso
from pydantic import BaseModel

router = APIRouter(prefix="/api/auth", tags=["Autenticación"])


class UsuarioRegistro(BaseModel):
    nombre: str
    contrasenia: str
    rol_id: int = 1  # Por defecto Administrador o el ID que manejes


@router.post("/register", status_code=201)
def registrar_usuario(user_in: UsuarioRegistro, db: Session = Depends(get_db)):
    # Verificar si el usuario ya existe
    existe = db.query(Usuario).filter(Usuario.nombre == user_in.nombre).first()
    if existe:
        raise HTTPException(status_code=400, detail="El nombre de usuario ya está registrado")

    # Verificar si el rol existe
    rol = db.get(Rol, user_in.rol_id)
    if not rol:
        raise HTTPException(status_code=400, detail="El Rol especificado no existe")

    # Guardar usuario con contraseña encriptada
    nuevo_usuario = Usuario(
        nombre=user_in.nombre,
        contrasenia=hashear_contrasenia(user_in.contrasenia),
        rol_id=user_in.rol_id
    )
    db.add(nuevo_usuario)
    db.commit()
    return {"message": "Usuario registrado con éxito"}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.nombre == form_data.username).first()
    if not usuario or not verificar_contrasenia(form_data.password, usuario.contrasenia):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generar el Token (guardamos el nombre en el "sub")
    access_token = crear_token_acceso(data={"sub": usuario.nombre})
    return {"access_token": access_token, "token_type": "bearer"}