from backend.models.Usuario import Usuario


class Vendedor(Usuario):
    def __init__(self, id, nombre, usuario, contrasenia, rol):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.rol = rol

    def obtener_rol(self):
        return "Vendedor"

    def registrar_venta(self, prenda, cantidad):
        total = prenda.precio_base * cantidad
        print(f"Venta registrada: {cantidad} x {prenda.nombre}. Total: ${total}")

    def consultar_disponibilidad(self, nombre_prenda):
        print(f"Buscando: {nombre_prenda}")