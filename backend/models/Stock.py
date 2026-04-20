from datetime import datetime

class Stock:
    def __init__(self, id, fecha, tipo, cantidad, usuario, prenda):
        self.id = id
        self.fecha = datetime.fromisoformat(fecha)
        self.tipo = tipo
        self.cantidad = cantidad
        self.usuario = usuario
        self.prenda = prenda


    def aumentar(self, cantidad: int):
        self.cantidad_actual += cantidad

    def disminuir(self, cantidad: int):
        if cantidad <= self.cantidad_actual:
            self.cantidad_actual -= cantidad
            return True
        return False

    def esta_bajo_stock(self) -> bool:
        return self.cantidad_actual <= self.punto_reposicion