# Taller mecánico

Aplicación de escritorio en Python para registrar clientes, vehículos y reparaciones de un taller mecánico. La interfaz está hecha con [Flet](https://flet.dev) y los datos se guardan en una base de datos SQLite.

## Características

- Formulario único para registrar cliente, vehículo y reparación.
- Validaciones en las clases de dominio (placa de 6 caracteres, costo no negativo, estado válido, descripción obligatoria).
- Cálculo del total con IVA del 19 %.
- Los tres registros se guardan en una sola transacción: si algo falla, no queda nada guardado a medias.
- Creación automática de las tablas al iniciar la aplicación.

## Requisitos

- Python 3.10 o superior
- Flet

```bash
pip install flet
```

## Ejecución

```bash
python main.py
```

Al iniciar se crea el archivo `inventario_master.db` en la carpeta del proyecto.

## Estructura del proyecto

```
.
├── main.py
├── data/
│   ├── database_manager.py
│   ├── cliente_dao.py
│   └── taller_repository.py
└── domain/
    ├── cliente.py
    └── reparacion.py
```

Ajusta los nombres de archivo si en tu proyecto son distintos.

| Módulo | Descripción |
|---|---|
| `main.py` | Interfaz Flet y registro de los datos en una transacción. |
| `data/database_manager.py` | `DatabaseManager`: context manager de SQLite con commit/rollback automático y claves foráneas activadas. Crea las tablas con `creador_tablas()`. |
| `data/cliente_dao.py` | `ClienteDAO`: agrega y consulta clientes. |
| `data/taller_repository.py` | `TallerRepository`: agrega y consulta reparaciones. |
| `domain/cliente.py` | Clase `Cliente`. |
| `domain/reparacion.py` | Clases `Vehiculo` y `Reparacion`. |

## Modelo de datos

```
clientes (id_cliente PK, nombre, telefono)
    └── vehiculos (id_vehiculo PK, placa UNIQUE, marca_modelo, id_cliente FK)
            └── reparaciones (id_reparacion PK, descripcion, costo_total, estado, id_vehiculo FK)
```

## Reglas de validación

| Campo | Regla |
|---|---|
| Placa | Exactamente 6 caracteres; se guarda en mayúsculas y debe ser única. |
| Descripción | No puede estar vacía. |
| Costo total | No puede ser negativo. |
| Estado | `pendiente`, `en proceso` o `completada`. |
| Id del vehículo | No puede ser negativo. |

## Notas

- En las versiones recientes de Flet (0.80 o superior) se usa `ft.run(main)`. En versiones anteriores, el equivalente es `ft.app(target=main)`.
- `Cliente` y `Vehiculo` comparan por su id y definen `__hash__`, por lo que pueden usarse en `set` y como claves de `dict`.