class Cliente:
    def __init__(self, id_cliente: int | None, nombre: str, telefono: str):
        self._id_cliente = id_cliente
        self.nombre = nombre
        self.telefono = telefono

    @property
    def id_cliente(self) -> int | None:
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, value: int | None):
        self._id_cliente = value

    @property
    def nombre(self) -> str:
        return self._nombre

    @nombre.setter
    def nombre(self, value: str):
        self._nombre = (value or "").strip()

    @property
    def telefono(self) -> str:
        return self._telefono

    @telefono.setter
    def telefono(self, value: str):
        self._telefono = (value or "").strip()

    def __str__(self) -> str:
        return f"Cliente(id_cliente={self.id_cliente}, nombre='{self.nombre}', telefono='{self.telefono}')"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Cliente):
            return NotImplemented
        return self.id_cliente == otro.id_cliente

    def __hash__(self) -> int:
        return hash(self.id_cliente)