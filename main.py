import flet as ft

from data.database_manager import DatabaseManager
from data.taller_repository import TallerRepository
from ui.app_view import TallerApp


def main(page: ft.Page):
    db = DatabaseManager()
    db.creador_tablas()

    taller_repository = TallerRepository(db)
    app = TallerApp(taller_repository)
    app.build(page)


if __name__ == "__main__":
    ft.run(main)