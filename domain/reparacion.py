class Vehiculo:
    def __init__(self, id_vehiculo: int, placa: str, marca_modelo: str, id_cliente: int):
        self._id_vehiculo = id_vehiculo
        self.placa = placa
        self.marca_modelo = marca_modelo
        self.id_cliente = id_cliente

    @property
    def id_vehiculo(self) -> int:
        return self._id_vehiculo

    @id_vehiculo.setter
    def id_vehiculo(self, value: int):
        self._id_vehiculo = value

    @property
    def placa(self) -> str:
        return self._placa

    @placa.setter
    def placa(self, value: str):
        verificar = (value or "").strip().upper()
        if len(verificar) != 6:
            raise ValueError("La placa debe tener exactamente 6 caracteres.")
        self._placa = verificar

    @property
    def marca_modelo(self) -> str:
        return self._marca_modelo

    @marca_modelo.setter
    def marca_modelo(self, value: str):
        self._marca_modelo = value

    @property
    def id_cliente(self) -> int:
        return self._id_cliente

    @id_cliente.setter
    def id_cliente(self, value: int):
        self._id_cliente = value

    def __str__(self) -> str:
        return f"Vehiculo(id_vehiculo={self.id_vehiculo}, placa='{self.placa}', marca_modelo='{self.marca_modelo}', id_cliente={self.id_cliente})"

    def __repr__(self) -> str:
        return self.__str__()

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Vehiculo):
            return NotImplemented
        if self.id_vehiculo != otro.id_vehiculo:
            return False
        return True

    def __hash__(self) -> int:
        return hash(self.id_vehiculo)


class Reparacion:
    _IVA: float = 0.19

    def __init__(self, id_reparacion: int, descripcion: str, costo_total: float, estado: str, id_vehiculo: int):
        self._id_reparacion = id_reparacion
        self.descripcion = descripcion
        self.costo_total = costo_total
        self.estado = estado
        self.id_vehiculo = id_vehiculo

    @property
    def id_reparacion(self) -> int:
        return self._id_reparacion

    @id_reparacion.setter
    def id_reparacion(self, value: int):
        self._id_reparacion = value

    @property
    def descripcion(self) -> str:
        return self._descripcion

    @descripcion.setter
    def descripcion(self, value: str):
        verificar = (value or "").strip()
        if not verificar:
            raise ValueError("La descripción no puede estar vacía.")
        self._descripcion = verificar

    @property
    def costo_total(self) -> float:
        return self._costo_total

    @costo_total.setter
    def costo_total(self, value: float):
        if value < 0:
            raise ValueError("El costo total no puede ser negativo.")
        self._costo_total = value

    @property
    def estado(self) -> str:
        return self._estado

    @estado.setter
    def estado(self, value: str):
        verificar = (value or "").strip().lower()
        if verificar not in ["pendiente", "en proceso", "completada"]:
            raise ValueError("El estado debe ser 'pendiente', 'en proceso' o 'completada'.")
        self._estado = verificar

    @property
    def id_vehiculo(self) -> int:
        return self._id_vehiculo

    @id_vehiculo.setter
    def id_vehiculo(self, value: int):
        if value < 0:
            raise ValueError("El id del vehículo no puede ser negativo.")
        self._id_vehiculo = value

    @property
    def total_iva(self) -> float:
        return round(self._costo_total * (1 + self._IVA), 2)

    def __float__(self) -> float:
        return self.total_iva

    def __str__(self) -> str:
        return f"Reparacion(id_reparacion={self.id_reparacion}, descripcion='{self.descripcion}', costo_total={self.costo_total}, estado='{self.estado}', id_vehiculo={self.id_vehiculo})"

    def __repr__(self) -> str:
        return self.__str__()