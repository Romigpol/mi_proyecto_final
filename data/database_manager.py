import sqlite3
from typing import Optional


class DatabaseManager:
    def __init__(self, db_path: str = "inventario_master.db") -> None:
        self.db_path: str = db_path
        self.__connection: Optional[sqlite3.Connection] = None
        self.__cursor: Optional[sqlite3.Cursor] = None

    def __enter__(self) -> sqlite3.Cursor:
        self.__connection = sqlite3.connect(self.db_path)
        self.__connection.execute("PRAGMA foreign_keys = ON;")
        self.__cursor = self.__connection.cursor()
        return self.__cursor

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[object],
    ) -> bool:
        if self.__connection:
            if exc_type is not None:
                self.__connection.rollback()
            else:
                self.__connection.commit()

            if self.__cursor:
                self.__cursor.close()
            self.__connection.close()
        return False

    def creador_tablas(self):
        with self as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehiculos (
                    id_vehiculo INTEGER PRIMARY KEY AUTOINCREMENT,
                    placa TEXT UNIQUE NOT NULL,
                    marca_modelo TEXT NOT NULL,
                    id_cliente INTEGER NOT NULL,
                    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS reparaciones (
                    id_reparacion INTEGER PRIMARY KEY AUTOINCREMENT,
                    descripcion TEXT NOT NULL,
                    costo_total REAL NOT NULL,
                    estado TEXT NOT NULL,
                    id_vehiculo INTEGER NOT NULL,
                    FOREIGN KEY (id_vehiculo) REFERENCES vehiculos(id_vehiculo)
                )
            """)

    def __repr__(self) -> str:
        return f"DatabaseManager(db_path='{self.db_path}')"