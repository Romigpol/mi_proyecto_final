class Cliente:
    def __init__(self, id_cliente: int, nombre: str, telefono: str):
        self._id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono

    @property
    def id_cliente(self) -> int:
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, value: int):
        self._id_cliente = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = value

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str):
        self._telefono = value

    def __str__(self) -> str:
        return f"Cliente(id_cliente={self.id_cliente}, nombre='{self.nombre}', telefono='{self.telefono}')"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return NotImplemented
        if self.id_cliente != otro.id_cliente:
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.id_cliente)