from backend.models.Rol import Rol

class Usuario(Rol):
    def _init_(self, id_usuario, nombre, contrasenia, rol):
        self.id = id_usuario
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.rol = Rol

    def login(self) -> bool:
        pass
