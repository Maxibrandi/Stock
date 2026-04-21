from datetime import datetime
from backend.models.Prenda import Prenda
from backend.models.Usuario import Usuario


class Venta:
    def _init_(self, id_venta, usuario, prenda, total):
        self.id = id_venta
        self.fecha = datetime.now()
        self.usuario = Usuario
        self.prendas = Prenda
        self.total = total

    def generar_reporte_rotacion(self):
        pass