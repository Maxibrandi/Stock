from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from database import get_db
from models import Prenda, PrendaCreate, PrendaUpdate

router = APIRouter(
    prefix="/prendas",
    tags=["Prendas"]
)


# 1. CREAR UNA PRENDA NEW
@router.post("/", response_model=Prenda, status_code=status.HTTP_201_CREATED)
def crear_prenda(prenda_in: PrendaCreate, db: Session = Depends(get_db)):
    # Verificamos si el código de barras ya está registrado (Regla de negocio: Debe ser único)
    statement = select(Prenda).where(Prenda.codigo_barras == prenda_in.codigo_barras)
    prenda_existente = db.exec(statement).first()

    if prenda_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ya existe una prenda registrada con el código de barras '{prenda_in.codigo_barras}'."
        )

    # Convertimos el esquema de validación al modelo de la tabla de la DB
    nueva_prenda = Prenda.from_orm(prenda_in)
    db.add(nueva_prenda)
    db.commit()
    db.refresh(nueva_prenda)
    return nueva_prenda


# 2. LISTAR TODAS LAS PRENDAS (Con paginación básica por si el stock crece)
@router.get("/", response_model=List[Prenda])
def listar_prendas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    statement = select(Prenda).offset(skip).limit(limit)
    prendas = db.exec(statement).all()
    return prendas


# 3. BUSCAR POR CÓDIGO DE BARRAS (Esencial para el escáner del local)
@router.get("/buscar/{codigo_barras}", response_model=Prenda)
def buscar_por_codigo_barras(codigo_barras: str, db: Session = Depends(get_db)):
    statement = select(Prenda).where(Prenda.codigo_barras == codigo_barras)
    prenda = db.exec(statement).first()

    if not prenda:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró ninguna prenda con el código de barras '{codigo_barras}'."
        )
    return prenda


# 4. EDITAR PRENDA EXISTENTE
@router.put("/{prenda_id}", response_model=Prenda)
def actualizar_prenda(prenda_id: int, prenda_in: PrendaUpdate, db: Session = Depends(get_db)):
    prenda_db = db.get(Prenda, prenda_id)
    if not prenda_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La prenda que intentas editar no existe."
        )

    # Extraemos solo los campos que envió el cliente para actualizar de forma parcial
    datos_actualizar = prenda_in.dict(exclude_unset=True)

    # Si intentan cambiar el código de barras, validamos que no colisione con otra prenda
    if "codigo_barras" in datos_actualizar and datos_actualizar["codigo_barras"] != prenda_db.codigo_barras:
        statement = select(Prenda).where(Prenda.codigo_barras == datos_actualizar["codigo_barras"])
        colision = db.exec(statement).first()
        if colision:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo código de barras ya está asignado a otra prenda."
            )

    for key, value in datos_actualizar.items():
        setattr(prenda_db, key, value)

    db.add(prenda_db)
    db.commit()
    db.refresh(prenda_db)
    return prenda_db


# 5. ELIMINAR PRENDA
@router.delete("/{prenda_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_prenda(prenda_id: int, db: Session = Depends(get_db)):
    prenda_db = db.get(Prenda, prenda_id)
    if not prenda_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La prenda que intentas eliminar no existe."
        )
    db.delete(prenda_db)
    db.commit()
    return None