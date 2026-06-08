# /app/routes/reportes.py
from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import List, Dict, Any
from models.bd import get_db, Prenda, Venta, DetalleVenta
from libs.seguridad import verificar_permiso_ganancias, verificar_es_administrador, Usuario

router = APIRouter(prefix="/api/reportes", tags=["Reportes & Dashboard"])

@router.get("/stock-critico", response_model=List[Prenda])
def obtener_prendas_en_alerta(
    db: Session = Depends(get_db),
    usuario_actual: Usuario = Depends(verificar_permiso_ganancias) # Vendedores y admins pueden ver stock
):
    """
    Retorna la lista de prendas cuyo stock actual es igual o menor al stock mínimo configurado.
    """
    statement = select(Prenda).where(Prenda.stock_actual <= Prenda.stock_minimo)
    return db.exec(statement).all()


@router.get("/dashboard-financiero")
def obtener_metricas_dashboard(
    db: Session = Depends(get_db),
    admin_actual: Usuario = Depends(verificar_permiso_ganancias) # Protegido por rol financiero
):
    """
    Retorna métricas clave de rendimiento: Total recaudado, cantidad de ventas y top prendas más vendidas.
    """
    # 1. Total Recaudado e Historial de Ventas
    total_recaudado = db.exec(select(func.sum(Venta.total))).one() or 0.0
    cantidad_ventas = db.exec(select(func.count(Venta.id))).one() or 0

    # 2. Ranking de los 5 productos más vendidos (Top 5)
    # Agrupamos los detalles de venta por prenda_id sumando la cantidad vendida
    ranking_stmt = (
        select(DetalleVenta.prenda_id, func.sum(DetalleVenta.cantidad).label("total_vendido"))
        .group_by(DetalleVenta.prenda_id)
        .order_by(func.sum(DetalleVenta.cantidad).desc())
        .limit(5)
    )
    ranking_resultados = db.exec(ranking_stmt).all()

    # Formateamos el ranking para que el frontend reciba el nombre de la prenda y no solo el ID
    top_prendas = []
    for prenda_id, total_vendido in ranking_resultados:
        prenda = db.get(Prenda, prenda_id)
        if prenda:
            top_prendas.append({
                "prenda_id": prenda.id,
                "nombre": prenda.nombre,
                "categoria": prenda.categoria,
                "talle": prenda.talle,
                "unidades_vendidas": total_vendido
            })

    return {
        "resumen": {
            "total_ingresos": total_recaudado,
            "cantidad_operaciones": cantidad_ventas
        },
        "top_productos": top_prendas
    }