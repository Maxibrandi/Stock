from datetime import datetime
from backend.models.Prenda import Prenda
from backend.models.Usuario import Usuario

class Movimiento:
    def _init_(self, id_mov, nombre, prenda, usuario, tipo, cantidad):
        self.id = id_mov
        self.fecha = datetime.now()
        self.prenda = Prenda
        self.nombre = Prenda
        self.usuario = Usuario
        self.tipo = tipo
        self.cantidad = cantidad

    def registrar_log(self):
        print(f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {self.tipo}: "
              f"{self.cantidad} unidades de {self.prenda.nombre} por {self.usuario.nombre}")