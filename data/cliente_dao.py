from domain.cliente import Cliente
from data.database_manager import DatabaseManager

class ClienteDAO:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def agregar_cliente(self, cliente: Cliente) -> int:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO clientes (nombre, telefono) VALUES (?, ?)",
                (cliente.nombre, cliente.telefono)
            )
            return cursor.lastrowid

    def obtener_cliente_por_id(self, id_cliente: int) -> Cliente | None:
        with self.db_manager as cursor:
            cursor.execute(
                "SELECT id_cliente, nombre, telefono FROM clientes WHERE id_cliente = ?",
                (id_cliente,)
            )
            row = cursor.fetchone()
            if row:
                return Cliente(id_cliente=row[0], nombre=row[1], telefono=row[2])
            return None

    def __len__(self) -> int:
        with self.db_manager as cursor:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            count = cursor.fetchone()[0]
            return count