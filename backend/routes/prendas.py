from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
# Asegurate de importar bien la ruta a tu archivo de modelos
from models.bd import get_db, Prenda, PrendaCreate, PrendaUpdate
from libs.seguridad import verificar_es_administrador, Usuario

router = APIRouter(prefix="/api/prendas", tags=["Prendas"])


@router.get("/", response_model=List[Prenda])
def listar_prendas(db: Session = Depends(get_db)):
    # SQLModel nativo usando db.exec y select
    prendas = db.exec(select(Prenda)).all()
    return prendas


@router.post("/", response_model=Prenda)
def crear_prenda(
    prenda_in: PrendaCreate,
    db: Session = Depends(get_db),
    admin_actual: Usuario = Depends(verificar_es_administrador) # <-- RESTRICCIÓN DE ROL ACTIVA
):
    # Si llega acá, FastAPI ya validó el Token Y que el usuario es Administrador
    db_prenda = Prenda.model_validate(prenda_in)
    db.add(db_prenda)
    db.commit()
    db.refresh(db_prenda)
    return db_prenda