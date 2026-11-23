from domain.cliente import Cliente
from data.database_manager import DatabaseManager


class ClienteDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def agregar_cliente(self, cliente: Cliente) -> int:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono),
            )
            return cursor.lastrowid

    def obtener_cliente_por_id(self, id_cliente: int) -> Cliente | None:
        with self.db_manager as cursor:
            cursor.execute(
                "SELECT id_cliente, nombre, telefono FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            )
            row = cursor.fetchone()
            if row:
                return Cliente(id_cliente=row[0], nombre=row[1], telefono=row[2])
            return None

    def actualizar_cliente(self, cliente: Cliente) -> bool:
        if cliente.id_cliente is None:
            raise ValueError("El cliente debe tener id_cliente para actualizarse.")
        with self.db_manager as cursor:
            cursor.execute(
                "UPDATE clientes SET nombre = ?, telefono = ? WHERE id_cliente = ?",
                (cliente.nombre, cliente.telefono, cliente.id_cliente),
            )
            return cursor.rowcount > 0

    def eliminar_cliente(self, id_cliente: int) -> bool:
        with self.db_manager as cursor:
            cursor.execute(
                "DELETE FROM clientes WHERE id_cliente = ?",
                (id_cliente,),
            )
            return cursor.rowcount > 0

    def __len__(self) -> int:
        with self.db_manager as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            count = cursor.fetchone()[0]
            return count