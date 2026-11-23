from domain.cliente import Cliente
from domain.reparacion import Vehiculo, Reparacion
from data.database_manager import DatabaseManager
from data.cliente_dao import ClienteDAO


class TallerRepository:
    PK_MAP = {
        "reparaciones": "id_reparacion",
        "vehiculos": "id_vehiculo",
        "clientes": "id_cliente",
    }

    def __init__(self, db_manager: DatabaseManager, cliente_dao: ClienteDAO | None = None):
        self.db_manager = db_manager
        self.cliente_dao = cliente_dao or ClienteDAO(db_manager)

    def agregar_cliente(self, cliente: Cliente) -> int:
        return self.cliente_dao.agregar_cliente(cliente)

    def agregar_vehiculo(self, vehiculo: Vehiculo) -> int:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO vehiculos (placa, marca_modelo, id_cliente) VALUES (?, ?, ?)",
                (vehiculo.placa, vehiculo.marca_modelo, vehiculo.id_cliente),
            )
            return cursor.lastrowid

    def agregar_reparacion(self, reparacion: Reparacion) -> int:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO reparaciones (descripcion, costo_total, estado, id_vehiculo) VALUES (?, ?, ?, ?)",
                (reparacion.descripcion, reparacion.costo_total, reparacion.estado, reparacion.id_vehiculo),
            )
            return cursor.lastrowid

    def registrar_reparacion(self, reparacion: Reparacion) -> int:
        return self.agregar_reparacion(reparacion)

    def obtener_reparacion_por_id(self, id_reparacion: int) -> Reparacion | None:
        with self.db_manager as cursor:
            cursor.execute(
                "SELECT id_reparacion, descripcion, costo_total, estado, id_vehiculo FROM reparaciones WHERE id_reparacion = ?",
                (id_reparacion,),
            )
            row = cursor.fetchone()
            if row:
                return Reparacion(
                    id_reparacion=row[0],
                    descripcion=row[1],
                    costo_total=row[2],
                    estado=row[3],
                    id_vehiculo=row[4],
                )
            return None

    def guardar_orden_completa(
        self, cliente: Cliente, vehiculo: Vehiculo, reparacion: Reparacion
    ) -> tuple[int, int, int]:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono),
            )
            id_cliente = cursor.lastrowid
            cliente.id_cliente = id_cliente

            vehiculo.id_cliente = id_cliente
            cursor.execute(
                "INSERT INTO vehiculos (placa, marca_modelo, id_cliente) VALUES (?, ?, ?)",
                (vehiculo.placa, vehiculo.marca_modelo, vehiculo.id_cliente),
            )
            id_vehiculo = cursor.lastrowid
            vehiculo.id_vehiculo = id_vehiculo

            reparacion.id_vehiculo = id_vehiculo
            cursor.execute(
                "INSERT INTO reparaciones (descripcion, costo_total, estado, id_vehiculo) VALUES (?, ?, ?, ?)",
                (reparacion.descripcion, reparacion.costo_total, reparacion.estado, reparacion.id_vehiculo),
            )
            id_reparacion = cursor.lastrowid
            reparacion.id_reparacion = id_reparacion

            return id_cliente, id_vehiculo, id_reparacion

    def listar_tabla(self, tabla: str) -> tuple[list[str], list[tuple]]:
        if tabla not in self.PK_MAP:
            raise ValueError(f"Tabla no permitida: {tabla}")
        with self.db_manager as cursor:
            cursor.execute(f"SELECT * FROM {tabla}")
            cols = [c[0] for c in cursor.description]
            filas = cursor.fetchall()
            return cols, filas

    def actualizar_registro(
        self,
        tabla: str,
        registro_id: int,
        nombre: str = "",
        telefono: str = "",
        placa: str = "",
        marca_modelo: str = "",
        descripcion: str = "",
        costo: float = 0.0,
        estado: str = "pendiente",
    ) -> bool:
        if tabla not in self.PK_MAP:
            raise ValueError(f"Tabla no permitida: {tabla}")
        with self.db_manager as cursor:
            if tabla == "reparaciones":
                rep = Reparacion(registro_id, descripcion, float(costo), estado, 0)
                cursor.execute(
                    "UPDATE reparaciones SET descripcion = ?, costo_total = ?, estado = ? WHERE id_reparacion = ?",
                    (rep.descripcion, rep.costo_total, rep.estado, registro_id),
                )
            elif tabla == "vehiculos":
                veh = Vehiculo(registro_id, placa, marca_modelo, 0)
                cursor.execute(
                    "UPDATE vehiculos SET placa = ?, marca_modelo = ? WHERE id_vehiculo = ?",
                    (veh.placa, veh.marca_modelo, registro_id),
                )
            elif tabla == "clientes":
                cli = Cliente(registro_id, nombre, telefono)
                cursor.execute(
                    "UPDATE clientes SET nombre = ?, telefono = ? WHERE id_cliente = ?",
                    (cli.nombre, cli.telefono, registro_id),
                )
            return cursor.rowcount > 0

    def eliminar_registro(self, tabla: str, registro_id: int) -> bool:
        if tabla not in self.PK_MAP:
            raise ValueError(f"Tabla no permitida: {tabla}")
        pk = self.PK_MAP[tabla]
        with self.db_manager as cursor:
            cursor.execute(f"DELETE FROM {tabla} WHERE {pk} = ?", (int(registro_id),))
            return cursor.rowcount > 0

    def __len__(self) -> int:
        with self.db_manager as cursor:
            cursor.execute("SELECT COUNT(*) FROM reparaciones")
            count = cursor.fetchone()[0]
            return count