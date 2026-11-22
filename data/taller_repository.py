from domain.reparacion import Reparacion
from data.database_manager import DatabaseManager

class TallerRepository:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def registrar_reparacion(self, reparacion: Reparacion) -> int:
        with self.db_manager as cursor:
            cursor.execute(
                "INSERT INTO reparaciones (descripcion, costo_total, estado, id_vehiculo) VALUES (?, ?, ?, ?)",
                (reparacion.descripcion, reparacion.costo_total, reparacion.estado, reparacion.id_vehiculo)
            )
            return cursor.lastrowid
    def obtener_reparacion_por_id(self, id_reparacion: int) -> Reparacion | None:
        with self.db_manager as cursor:
            cursor.execute(
                "SELECT id_reparacion, descripcion, costo_total, estado, id_vehiculo FROM reparaciones WHERE id_reparacion = ?",
                (id_reparacion,)
            )
            row = cursor.fetchone()
            if row:
                return Reparacion(id_reparacion=row[0], descripcion=row[1], costo_total=row[2], estado=row[3], id_vehiculo=row[4])
            return None
    def __len__(self) -> int:
        with self.db_manager as cursor:
            cursor.execute("SELECT COUNT(*) FROM reparaciones")
            count = cursor.fetchone()[0]
            return count