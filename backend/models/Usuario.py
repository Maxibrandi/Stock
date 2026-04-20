from abc import ABC, abstractmethod

class Usuario(ABC):
    @abstractmethod
    def __init__(self, id, nombre, usuario, contrasenia, rol):
        self.id = id
        self.nombre = nombre
        self.usuario = usuario
        self.contrasenia = contrasenia
        self.rol = rol

    def __str__(self):
        return f"Usuario(ID: {self.id}, Usuario: {self.usuario} Nombre: {self.nombre}, Rol: {self.rol})"

