# models.py
# Prepara las opciones del menú seleccionar. Crea las clases de datos

from __future__ import annotations # Para usar tipos de datos que todavía se
# están escribiendo en el mismo archivo

import uuid

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import List


# ==========================================
# EXCEPCIONES DE DOMINIO
# ==========================================
# ¿Por qué excepciones propias?: Separamos los errores técnicos (ej. un fallo de red o un KeyError)
# de los errores de negocio. Esto permite que las capas superiores (como la interfaz de usuario)
# atrapen estas excepciones específicas y muestren mensajes limpios al operador sin romper el programa.
class DomainException(Exception):
    """Excepción base para reglas de negocio."""
    pass


class EstadoInvalidoException(DomainException):
    """Lanzada cuando se intenta una transición de estado ilegal."""
    pass


class ClienteNoEncontradoException(DomainException):
    """Lanzada cuando una búsqueda en el repositorio falla."""
    pass


# ==========================================
# VALUE OBJECTS (ENUMS)
# ==========================================
# ¿Por qué Enums?: Evitamos el uso de "cadenas mágicas" (strings sueltos como "CABA" o "AEREO").
# Las cadenas son propensas a errores de tipeo. Al usar Enums, restringimos los valores posibles
# desde la raíz. Si el negocio pide agregar un nuevo destino, solo agregamos una línea acá (Principio OCP).
class Destino(Enum):
    CABA = auto()
    AMBA = auto()
    CENTRO = auto()
    COSTA = auto()
    NORTE = auto()
    SUR = auto()


class CategoriaPeso(Enum):
    LIGERO = auto()
    MEDIO = auto()
    PESADO = auto()


class TipoServicio(Enum):
    ESTANDAR = auto()
    URGENTE = auto()
    AEREO = auto()
    FRAGIL = auto()

# ==========================================
# PATRÓN STATE (MÁQUINA DE ESTADOS)
# ==========================================

# ¿Por qué el Patrón State?: En vez de llenar la clase Encomienda con múltiples 'if'
# (ej. if estado == "En Depósito"), delegamos el comportamiento a clases individuales.
# Esto garantiza Alta Cohesión: cada estado sabe exactamente a qué estado le toca ir después y rechaza
# transiciones ilógicas por sí mismo.
class IEstadoEncomienda(ABC):
    @abstractmethod
    def avanzar(self, contexto: 'Encomienda') -> None:
        """Transiciona al siguiente estado lógico."""
        pass

    @property
    @abstractmethod
    def nombre(self) -> str:
        """Devuelve el nombre legible del estado."""
        pass


class EstadoEntregado(IEstadoEncomienda):
    def avanzar(self, contexto: 'Encomienda') -> None:
        # Programación defensiva: Si alguien aprieta "avanzar" en un paquete entregado, el sistema lo frena.
        raise EstadoInvalidoException(
            "La encomienda ya fue entregada. Estado final.")

    @property
    def nombre(self) -> str:
        return "Entregado"


class EstadoEnTransito(IEstadoEncomienda):
    def avanzar(self, contexto: 'Encomienda') -> None:
        # El estado actual inyecta el nuevo estado en el contexto de la encomienda.
        contexto.set_estado(EstadoEntregado())

    @property
    def nombre(self) -> str:
        return "En Tránsito"


class EstadoEnDeposito(IEstadoEncomienda):
    def avanzar(self, contexto: 'Encomienda') -> None:
        contexto.set_estado(EstadoEnTransito())

    @property
    def nombre(self) -> str:
        return "En Depósito"


# ==========================================
# ENTIDADES DE DOMINIO
# ==========================================
# ¿Por qué @dataclass?: Nos ahorra escribir métodos repetitivos como __init__ o __repr__.
# Es ideal para clases que son primordialmente contenedores de datos, asegurando un tipado estricto.
@dataclass
class Cliente:
    dni: str
    nombre: str
    contacto: str
    # Generamos un UUID automáticamente al instanciar para garantizar identidad única en la base de datos.
    id: str = field(default_factory=lambda: str(uuid.uuid4()))


@dataclass
class Cotizacion:
    subtotal: float = 0.0
    recargos: float = 0.0
    iva: float = 0.0

    # ¿Por qué @property?: Protege el cálculo. El total no se puede modificar manualmente desde afuera.
    # Siempre será la suma matemática exacta de los atributos internos, garantizando consistencia.
    @property
    def total(self) -> float:
        """Calcula el total al vuelo asegurando consistencia."""
        return self.subtotal + self.recargos + self.iva


# ¿Por qué una clase normal y no @dataclass acá?: Porque Encomienda tiene lógica interna de inicialización
# (como recortar el UUID a 8 caracteres para el tracking) y atributos privados manejados por propiedades,
# lo cual excede el propósito de un simple contenedor de datos.
class Encomienda:
    def __init__(self, cliente_id: str, destino: Destino, peso: CategoriaPeso,
                 servicios: List[TipoServicio]):
        # Encapsulamiento: Usamos el guion bajo (_) para indicar que estos atributos son de uso interno.
        self._tracking_id: str = str(uuid.uuid4())[:8].upper()
        self._cliente_id: str = cliente_id
        self._destino: Destino = destino
        self._peso: CategoriaPeso = peso
        self._servicios: List[TipoServicio] = servicios
        # Regla de negocio: Toda encomienda nace obligatoriamente en el depósito.
        self._estado: IEstadoEncomienda = EstadoEnDeposito()

    # Exponemos los datos de forma de solo lectura a través de propiedades.
    @property
    def tracking_id(self) -> str:
        return self._tracking_id

    @property
    def cliente_id(self) -> str:
        return self._cliente_id

    @property
    def servicios(self) -> List[TipoServicio]:
        return self._servicios

    @property
    def destino(self) -> Destino:
        return self._destino

    @property
    def peso(self) -> CategoriaPeso:
        return self._peso

    def estado_actual(self) -> str:
        return self._estado.nombre

    def set_estado(self, nuevo_estado: IEstadoEncomienda) -> None:
        """Usado internamente por las clases de Estado para mutar el contexto."""
        self._estado = nuevo_estado

    def avanzar_estado(self) -> None:
        """Delega la lógica de transición al estado actual."""
        self._estado.avanzar(self)


@dataclass
class Factura:
    cliente: Cliente
    detalle: Encomienda
    cotizacion: Cotizacion
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    fecha_emision: datetime = field(default_factory=datetime.now)