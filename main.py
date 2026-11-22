import flet as ft

from data.database_manager import DatabaseManager
from domain.cliente import Cliente
from domain.reparacion import Vehiculo, Reparacion


def main(page: ft.Page):
    db = DatabaseManager()
    db.creador_tablas()

    page.title = "Taller mecánico"
    nombre = ft.TextField(label="Nombre del cliente")
    telefono = ft.TextField(label="Teléfono")
    placa = ft.TextField(label="Placa (6 caracteres)", max_length=6)
    marca_modelo = ft.TextField(label="Marca y modelo")
    descripcion = ft.TextField(label="Descripción")
    costo = ft.TextField(label="Costo total")
    estado = ft.Dropdown(
        label="Estado",
        value="pendiente",
        options=[ft.dropdown.Option(x) for x in ("pendiente", "en proceso", "completada")],
    )
    mensaje = ft.Text()

    def guardar(e):
        try:
            cliente = Cliente(None, nombre.value, telefono.value)
            vehiculo = Vehiculo(None, placa.value, marca_modelo.value, None)
            reparacion = Reparacion(None, descripcion.value, float(costo.value), estado.value, 0)

            with db as cursor:
                cursor.execute(
                    "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                    (cliente.nombre, cliente.telefono),
                )
                vehiculo.id_cliente = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO vehiculos (placa, marca_modelo, id_cliente) VALUES (?, ?, ?)",
                    (vehiculo.placa, vehiculo.marca_modelo, vehiculo.id_cliente),
                )
                reparacion.id_vehiculo = cursor.lastrowid
                cursor.execute(
                    "INSERT INTO reparaciones (descripcion, costo_total, estado, id_vehiculo) VALUES (?, ?, ?, ?)",
                    (reparacion.descripcion, reparacion.costo_total, reparacion.estado, reparacion.id_vehiculo),
                )

            for campo in (nombre, telefono, placa, marca_modelo, descripcion, costo):
                campo.value = ""
            mensaje.value = f"Guardado. Total con IVA: {reparacion.total_iva:,.2f}"
            mensaje.color = ft.Colors.GREEN
        except Exception as ex:
            mensaje.value = f"Error: {ex}"
            mensaje.color = ft.Colors.RED
        page.update()

    page.add(
        nombre, telefono, placa, marca_modelo, descripcion, costo, estado,
        ft.Button("Guardar", on_click=guardar),
        mensaje,
    )


if __name__ == "__main__":
    ft.run(main)