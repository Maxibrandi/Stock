class Prenda:
    def __init__(self, id_prenda, nombre, codigo_barras, talle, tipo_tela, precio, stock_minimo):
        self.id = id_prenda
        self.nombre = nombre
        self.codigo_barras = codigo_barras
        self.talle = talle
        self.tipo_tela = tipo_tela
        self.precio = precio
        self.stock_actual = 0
        self.stock_minimo = stock_minimo

    def verificar_alerta_stock(self) -> bool:
        return self.stock_actual <= self.stock_minimo