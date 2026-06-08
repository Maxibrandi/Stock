from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from models.bd import get_db, Venta, DetalleVenta, Prenda, VentaCreate
from libs.seguridad import obtener_usuario_actual, Usuario, verificar_permiso_ganancias

router = APIRouter(prefix="/api/ventas", tags=["Ventas"])


@router.post("/", response_model=Venta)
def registrar_venta(
        venta_in: VentaCreate,
        db: Session = Depends(get_db),
        usuario_actual: Usuario = Depends(obtener_usuario_actual)  # <-- INYECTAMOS EL USUARIO AUTENTICADO
):
    total_venta = 0.0
    detalles_a_guardar = []
    prendas_a_actualizar = []

    for item in venta_in.items:
        prenda = db.get(Prenda, item.prenda_id)
        if not prenda:
            raise HTTPException(status_code=404, detail=f"La prenda con ID {item.prenda_id} no existe.")

        if prenda.stock_actual < item.cantidad:
            raise HTTPException(status_code=400, detail=f"Stock insuficiente para '{prenda.nombre}'.")

        prenda.stock_actual -= item.cantidad
        prendas_a_actualizar.append(prenda)

        subtotal = prenda.precio * item.cantidad
        total_venta += subtotal

        detalle = DetalleVenta(
            prenda_id=item.prenda_id,
            cantidad=item.cantidad,
            precio_unitario=prenda.precio
        )
        detalles_a_guardar.append(detalle)

    # 2. Reemplazamos venta_in.usuario_id por el ID REAL del token
    db_venta = Venta(
        usuario_id=usuario_actual.id,  # <-- AQUÍ USAMOS EL USUARIO REAL DEL TOKEN
        total=total_venta
    )
    db.add(db_venta)
    db.commit()
    db.refresh(db_venta)

    for detalle in detalles_a_guardar:
        detalle.venta_id = db_venta.id
        db.add(detalle)

    for prenda in prendas_a_actualizar:
        db.add(prenda)
        prenda.verificar_alerta_stock()

    db.commit()
    return db_venta


@router.get("/", response_model=List[Venta])
def listar_ventas(db: Session = Depends(get_db)):
    return db.exec(select(Venta)).all()


@router.get("/reporte-financiero")
def obtener_reporte_ganancias(
        db: Session = Depends(get_db),
        usuario_autorizado: Usuario = Depends(verificar_permiso_ganancias)  # <-- VALIDA EL BOOLEANO DEL ROL
):
    # Cálculo rápido de todo lo recaudado en la tabla de ventas
    from sqlmodel import func
    total_recaudado = db.query(func.sum(Venta.total)).scalar() or 0.0

    return {
        "mensaje": f"Hola {usuario_autorizado.nombre}, acceso concedido al reporte.",
        "total_ventas_historico": total_recaudado
    }