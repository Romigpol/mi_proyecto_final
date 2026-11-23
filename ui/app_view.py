import flet as ft

from domain.cliente import Cliente
from domain.reparacion import Vehiculo, Reparacion
from data.taller_repository import TallerRepository


class TallerApp:
    def __init__(self, taller_repository: TallerRepository):
        self.repo = taller_repository
        self.page: ft.Page | None = None

        self.txt_id = ft.TextField(label="ID para editar o borrar", width=210)
        self.txt_nombre = ft.TextField(label="Nombre del cliente")
        self.txt_telefono = ft.TextField(label="Teléfono")
        self.txt_placa = ft.TextField(label="Placa (6 caracteres)", max_length=6)
        self.txt_marca_modelo = ft.TextField(label="Marca y modelo")
        self.txt_descripcion = ft.TextField(label="Descripción")
        self.txt_costo = ft.TextField(label="Costo sin IVA")
        self.dd_estado = ft.Dropdown(
            label="Estado",
            value="pendiente",
            options=[ft.dropdown.Option(x) for x in ("pendiente", "en proceso", "completada")],
        )
        self.lbl_estado = ft.Text()

        self.dd_tabla = ft.Dropdown(
            label="Tabla",
            value="reparaciones",
            options=[ft.dropdown.Option(t) for t in TallerRepository.PK_MAP],
            on_change=self.cargar_datos,
        )
        self.area_tabla = ft.Container()

    def build(self, page: ft.Page):
        self.page = page
        self.page.title = "Taller mecánico"
        self.page.scroll = ft.ScrollMode.AUTO

        self.page.add(
            self.txt_id, self.txt_nombre, self.txt_telefono, self.txt_placa,
            self.txt_marca_modelo, self.txt_descripcion, self.txt_costo, self.dd_estado,
            ft.Row([
                ft.Button("Guardar", on_click=self.guardar_datos),
                ft.Button("Actualizar", on_click=self.actualizar_datos),
                ft.Button("Borrar ID", on_click=self.borrar_por_id),
                ft.Button("Limpiar", on_click=self.limpiar_formulario),
            ], wrap=True),
            self.lbl_estado,
            ft.Divider(),
            ft.Row([self.dd_tabla, ft.Button("Actualizar vista", on_click=self.cargar_datos)]),
            ft.Row([self.area_tabla], scroll=ft.ScrollMode.AUTO),
        )
        self.cargar_datos()

    def aviso(self, texto: str, color):
        self.lbl_estado.value = texto
        self.lbl_estado.color = color
        self.page.update()

    def leer_id(self) -> int:
        val = (self.txt_id.value or "").strip()
        if not val:
            raise ValueError("Falta el ID.")
        return int(val)

    def limpiar_formulario(self, e=None):
        self.txt_id.value = ""
        for c in (self.txt_nombre, self.txt_telefono, self.txt_placa, self.txt_marca_modelo, self.txt_descripcion, self.txt_costo):
            c.value = ""
        self.dd_estado.value = "pendiente"
        if e is not None:
            self.page.update()

    def seleccionar_fila(self, tabla: str, fila: tuple):
        self.txt_id.value = str(fila[0])
        if tabla == "reparaciones":
            self.txt_descripcion.value, self.txt_costo.value, self.dd_estado.value = (
                str(fila[1] or ""), str(fila[2] if fila[2] is not None else ""), str(fila[3] or "pendiente")
            )
        elif tabla == "vehiculos":
            self.txt_placa.value, self.txt_marca_modelo.value = str(fila[1] or ""), str(fila[2] or "")
        elif tabla == "clientes":
            self.txt_nombre.value, self.txt_telefono.value = str(fila[1] or ""), str(fila[2] or "")
        self.aviso(f"Cargado registro #{fila[0]} ({tabla})", ft.Colors.BLUE)

    def borrar_registro(self, tabla: str, reg_id: int):
        ok = self.repo.eliminar_registro(tabla, int(reg_id))
        self.limpiar_formulario()
        self.aviso(
            f"Registro #{reg_id} eliminado de {tabla}" if ok else f"No se encontró el registro #{reg_id} en {tabla}",
            ft.Colors.ORANGE if ok else ft.Colors.RED,
        )
        self.cargar_datos()

    def borrar_por_id(self, e=None):
        try:
            self.borrar_registro(self.dd_tabla.value or "reparaciones", self.leer_id())
        except Exception as err:
            self.aviso(f"Error: {err}", ft.Colors.RED)

    def cargar_datos(self, e=None):
        tabla = self.dd_tabla.value or "reparaciones"
        try:
            cols, regs = self.repo.listar_tabla(tabla)
            filas = []
            for r in regs:
                celdas = [
                    ft.DataCell(ft.Text(str(
                        Reparacion(None, "item", float(d), "pendiente", 0).total_iva
                        if tabla == "reparaciones" and c == "costo_total" and d is not None
                        else ("" if d is None else d)
                    )))
                    for c, d in zip(cols, r)
                ]
                celdas.append(ft.DataCell(ft.Row([
                    ft.Button("Editar", on_click=lambda e, tb=tabla, fl=r: self.seleccionar_fila(tb, fl)),
                    ft.Button("Borrar", on_click=lambda e, tb=tabla, rid=r[0]: self.borrar_registro(tb, rid)),
                ], spacing=6)))
                filas.append(ft.DataRow(cells=celdas))

            self.area_tabla.content = ft.DataTable(
                columns=[ft.DataColumn(ft.Text(c)) for c in cols] + [ft.DataColumn(ft.Text("Acciones"))],
                rows=filas,
            )
            self.aviso(f"Tabla {tabla}: {len(regs)} filas", ft.Colors.BLUE)
        except Exception as err:
            self.aviso(f"Error: {err}", ft.Colors.RED)

    def guardar_datos(self, e=None):
        try:
            cliente = Cliente(None, self.txt_nombre.value, self.txt_telefono.value)
            vehiculo = Vehiculo(None, self.txt_placa.value, self.txt_marca_modelo.value, 0)
            reparacion = Reparacion(None, self.txt_descripcion.value, float(self.txt_costo.value), self.dd_estado.value, 0)
            self.repo.guardar_orden_completa(cliente, vehiculo, reparacion)
            self.limpiar_formulario()
            self.aviso(f"Guardado con éxito. Total IVA: {reparacion.total_iva:,.2f}", ft.Colors.GREEN)
            self.cargar_datos()
        except Exception as err:
            self.aviso(f"Error: {err}", ft.Colors.RED)

    def actualizar_datos(self, e=None):
        tabla = self.dd_tabla.value or "reparaciones"
        try:
            reg_id = self.leer_id()
            costo_val = float(self.txt_costo.value) if (self.txt_costo.value or "").strip() else 0.0
            ok = self.repo.actualizar_registro(
                tabla=tabla, registro_id=reg_id,
                nombre=self.txt_nombre.value, telefono=self.txt_telefono.value,
                placa=self.txt_placa.value, marca_modelo=self.txt_marca_modelo.value,
                descripcion=self.txt_descripcion.value, costo=costo_val,
                estado=self.dd_estado.value or "pendiente",
            )
            self.limpiar_formulario()
            self.aviso(
                f"Registro #{reg_id} actualizado en {tabla}" if ok else f"No se encontró el registro #{reg_id} en {tabla}",
                ft.Colors.GREEN if ok else ft.Colors.RED,
            )
            self.cargar_datos()
        except Exception as err:
            self.aviso(f"Error: {err}", ft.Colors.RED)