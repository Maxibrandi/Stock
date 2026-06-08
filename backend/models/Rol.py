class Rol:
    def __init__(self, id_rol: int, nombre_rol: str, puede_ver_ganancias: bool, puede_gestionar_stock: bool):
        self.id = id_rol
        self.nombre_rol = nombre_rol
        self.puede_ver_ganancias = puede_ver_ganancias
        self.puede_gestionar_stock = puede_gestionar_stock