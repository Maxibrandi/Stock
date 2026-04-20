from datetime import datetime
from backend.models.Prenda import Prenda
from backend.models.Usuario import Usuario

class Movimiento:
    def __init__(self, id_mov: int, prenda: Prenda, usuario: 'Usuario', tipo: str, cantidad: int):
        self.id = id_mov
        self.fecha = datetime.now()
        self.prenda = prenda
        self.usuario = usuario
        self.tipo = tipo
        self.cantidad = cantidad

    def registrar_log(self):
        print(f"[{self.fecha.strftime('%Y-%m-%d %H:%M')}] {self.tipo}: "
              f"{self.cantidad} unidades de {self.prenda.nombre} por {self.usuario.nombre}")