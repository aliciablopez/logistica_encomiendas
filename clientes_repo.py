import sqlite3
import os
from abc import ABC, abstractmethod
from models import Cliente, ClienteNoEncontradoException


class IRepoClientes(ABC):
    """Contrato que debe cumplir cualquier repositorio de clientes."""

    @abstractmethod
    def save(self, cliente: Cliente) -> None:
        pass

    @abstractmethod
    def find_by_dni(self, dni: str) -> Cliente:
        pass


class RepoClientes(IRepoClientes):
    """Implementación del repositorio usando una base de datos SQLite3 local."""

    def __init__(self, db_path: str = "logistica.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Crea la tabla de clientes y muestra la ruta absoluta para seguimiento."""
        print(
            f">> [DEBUG] Creando base de datos en: {os.path.abspath(self.db_path)}")
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                         CREATE TABLE IF NOT EXISTS clientes
                         (
                             id
                             TEXT
                             PRIMARY
                             KEY,
                             dni
                             TEXT
                             UNIQUE,
                             nombre
                             TEXT,
                             contacto
                             TEXT
                         )
                         """)
            conn.commit()

    def save(self, cliente: Cliente) -> None:
        """Guarda o actualiza un cliente en la base de datos."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT OR REPLACE INTO clientes (id, dni, nombre, contacto) VALUES (?, ?, ?, ?)",
                (cliente.id, cliente.dni, cliente.nombre, cliente.contacto)
            )
            conn.commit()

    def find_by_dni(self, dni: str) -> Cliente:
        """Busca un cliente por su DNI o lanza una excepción si no existe."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, dni, nombre, contacto FROM clientes WHERE dni = ?",
                (dni,))
            row = cursor.fetchone()

            if not row:
                raise ClienteNoEncontradoException(
                    f"No se encontró un cliente con el DNI: {dni}")

            return Cliente(
                id=row[0],
                dni=row[1],
                nombre=row[2],
                contacto=row[3]
            )