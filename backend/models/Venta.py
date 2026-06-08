from datetime import datetime
from backend.models.Prenda import Prenda
from backend.models.Usuario import Usuario
from backend.models.Movimientos import Movimiento

class Venta:
    def __init__(self, id_venta, usuario, prenda, total, movimiento):
        self.id = id_venta
        self.fecha = datetime.now()
        self.usuario = Usuario
        self.prendas = Prenda
        self.total = total
        self.movimiento = movimiento

    def agregar_prenda_por_scanner(self, prenda: Prenda):
        self.items.append(prenda)
        self.total += prenda.precio
        mov = Movimiento(None, prenda, self.usuario, "Salida", 1)
        mov.registrar_movimiento()

    def procesar_venta(self):
        print(f"Venta {self.id} procesada por {self.usuario.nombre}. Total: ${self.total}")