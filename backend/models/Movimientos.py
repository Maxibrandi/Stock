from datetime import datetime
from backend.models.Prenda import Prenda
from backend.models.Usuario import Usuario

class Movimiento:
    def __init__(self, id_mov, nombre, prenda, usuario, tipo, cantidad):
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


    def registrar_movimiento(self):
         if self.tipo.lower() == "entrada":
            self.prenda.stock_actual += self.cantidad
         elif self.tipo.lower() == "salida":
            self.prenda.stock_actual -= self.cantidad
            self.prenda.verify_alerta_stock()