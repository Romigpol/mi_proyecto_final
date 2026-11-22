from domain.cliente import Cliente
from domain.reparacion import Vehiculo, Reparacion


class TallerApp:
    def __init__(self, taller_repository):
        self.taller_repository = taller_repository

    def guardar_datos(self, e):
        cliente = Cliente(None, self.txt_nombre.value, self.txt_telefono.value)
        vehiculo = Vehiculo(None, self.txt_placa.value, self.txt_marca_modelo.value, None)

        id_cliente = self.taller_repository.agregar_cliente(cliente)
        vehiculo.id_cliente = id_cliente
        id_vehiculo = self.taller_repository.agregar_vehiculo(vehiculo)

        reparacion = Reparacion(
            None,
            self.txt_descripcion.value,
            float(self.txt_costo_total.value),
            self.txt_estado.value,
            id_vehiculo,
        )
        self.taller_repository.agregar_reparacion(reparacion)