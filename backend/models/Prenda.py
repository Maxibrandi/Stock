class Prenda:
    def __init__(self, id, nombre, descripcion, talle, tipo_tela, precio_costo, precio_venta, codigo_barras, stock, stock_min):
        self.id = id
        self.nombre = nombre
        self.descripcion = descripcion
        self.talle = talle
        self.tipo_tela = tipo_tela
        self.precio_costo = precio_costo
        self.precio_venta = precio_venta
        self.codigo_barras = codigo_barras
        self.stock = stock
        self.stock_min = stock_min

    def __str__(self):
        return (f"Prenda(la prenda{self.nombre}: {self.descripcion}, talle{self.talle}, tipo_tela{self.tipo_tela}"
                f"precio {self.precio_venta} fue agregada")

