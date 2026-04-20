from backend.models.Usuario import Usuario

class Administrador(Usuario):
    def __init__(self, id, nombre, usuario, contrasena, rol):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena
        self.rol = rol

    def obtener_rol(self):
        return "Administrador"



