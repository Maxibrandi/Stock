from .Rol import Rol

class Usuario:  # Quitamos la herencia (Rol) -> Ahora es composición pura
    def __init__(self, id_usuario: int, nombre: str, contrasenia: str, rol: Rol):
        self.id = id_usuario
        self.nombre = nombre
        self.contrasenia = contrasenia
        self.rol = rol  # Guardamos la instancia del Rol que recibe por parámetro

    def login(self, usuario_ingresado: str, clave_ingresada: str) -> bool:
        return self.nombre == usuario_ingresado and self.contrasenia == clave_ingresada
