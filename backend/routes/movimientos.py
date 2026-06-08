from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from models.bd import get_db, Movimiento, TipoMovimientoEnum, Prenda, MovimientoCreate
from libs.seguridad import obtener_usuario_actual, Usuario

router = APIRouter(prefix="/api/movimientos", tags=["Movimientos de Stock"])


@router.get("/", response_model=List[Movimiento])
def listar_historial_movimientos(
    prenda_id: Optional[int] = Query(None, description="Filtrar por el ID de una prenda específica"),
    tipo: Optional[TipoMovimientoEnum] = Query(None, description="Filtrar por 'entrada' o 'salida'"),
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Retorna el historial completo de movimientos de stock con filtros opcionales.
    """
    statement = select(Movimiento).order_by(Movimiento.fecha.desc())

    if prenda_id:
        statement = statement.where(Movimiento.prenda_id == prenda_id)
    if tipo:
        statement = statement.where(Movimiento.tipo == tipo)

    return db.exec(statement).all()


@router.post("/", response_model=Movimiento, status_code=status.HTTP_201_CREATED)
def registrar_movimiento(
    mov_in: MovimientoCreate,
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(obtener_usuario_actual)
):
    """
    Registra un nuevo movimiento de stock (entrada/salida), actualiza el inventario de la prenda
    y evalúa si se deben disparar alertas de stock mínimo.
    """
    # 1. Validar existencia de la prenda
    prenda = db.get(Prenda, mov_in.prenda_id)
    if not prenda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Prenda no encontrada")

    # 2. Modificar el stock según el tipo de movimiento
    if mov_in.tipo == TipoMovimientoEnum.entrada:
        prenda.stock_actual += mov_in.cantidad
    elif mov_in.tipo == TipoMovimientoEnum.salida:
        if prenda.stock_actual < mov_in.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Stock insuficiente para realizar la salida"
            )
        prenda.stock_actual -= mov_in.cantidad

    # 3. Crear el registro del movimiento asociando el ID del usuario autenticado
    db_movimiento = Movimiento(
        prenda_id=mov_in.prenda_id,
        tipo=mov_in.tipo,
        cantidad=mov_in.cantidad,
        usuario_id=usuario_actual.id  # Eliminado el hardcodeo, usamos el usuario real
    )

    db.add(db_movimiento)
    db.add(prenda)
    db.commit()
    db.refresh(db_movimiento)

    # 4. Verificar alertas de stock después de impactar los cambios
    prenda.verificar_alerta_stock()

    return db_movimiento