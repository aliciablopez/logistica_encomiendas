# clientes_repo.py
import sqlite3
from typing import Optional
from models import Cliente


class ClienteRepository:
    """
    Gestiona la persistencia de los datos de clientes en la base de datos SQLite.
    """

    def __init__(self, db_path: str = "database.db"):
        self.db_path = db_path
        self._crear_tabla_si_no_existe()

    def _obtener_conexion(self) -> sqlite3.Connection:
        """Abre una conexión activa hacia la base de datos database.db."""
        return sqlite3.connect(self.db_path)

    def _crear_tabla_si_no_existe(self) -> None:
        """Crea la tabla 'clientes' en la base de datos si no existe aún."""
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS clientes (
                    documento TEXT PRIMARY KEY,
                    nombre TEXT NOT NULL,
                    telefono TEXT NOT NULL,
                    email TEXT NOT NULL
                )
            """)
            conn.commit()

    def buscar_por_documento(self, documento: str) -> Optional[Cliente]:
        """
        READ: Busca un cliente por su número de documento.
        Retorna una instancia de Cliente si existe, o None si no se encuentra.
        """
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT documento, nombre, telefono, email FROM clientes WHERE documento = ?",
                (documento,)
            )
            fila = cursor.fetchone()

            if fila:
                return Cliente(
                    documento=fila[0],
                    nombre=fila[1],
                    telefono=fila[2],
                    email=fila[3]
                )
            return None

    def guardar(self, cliente: Cliente) -> None:
        """
        CREATE / UPDATE: Inserta un nuevo cliente o actualiza sus datos si ya existe.
        """
        with self._obtener_conexion() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (documento, nombre, telefono, email)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(documento) DO UPDATE SET
                    nombre=excluded.nombre,
                    telefono=excluded.telefono,
                    email=excluded.email
            """, (cliente.documento, cliente.nombre, cliente.telefono, cliente.email))
            conn.commit()