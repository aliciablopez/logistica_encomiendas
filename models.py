# models.py
from enum import Enum
from dataclasses import dataclass


# ==========================================
# 1. ENUMS (Opciones fijas del negocio)
# ==========================================

class ZonaDestino(Enum):
    CABA = "CABA"
    AMBA = "AMBA"
    CENTRO = "Centro"
    COSTA = "Costa"
    NORTE = "Norte"
    SUR = "Sur"

class CategoriaPeso(Enum):
    LIGERO = "Hasta 5 kg"
    MEDIO = "De 5 a 15 kg"
    PESADO = "Más de 15 kg"

class TipoServicio(Enum):
    ESTANDAR = "Estándar"
    URGENTE = "Urgente"
    AEREO = "Aéreo"
    FRAGIL = "Frágil"

class EstadoEncomienda(Enum):
    EN_DEPOSITO = "En Depósito"
    EN_TRANSITO = "En Tránsito"
    ENTREGADO = "Entregado"

# ==========================================
# 2. ENTIDADES DE DATOS
# ==========================================

@dataclass
class Cliente:
    """
    Representa la entidad Cliente en el sistema.

    Atributos:
        documento (str): DNI o CUIT. Actúa como identificador único (Clave Primaria).
        nombre (str): Nombre completo o Razón Social.
        telefono (str): Número de contacto.
        email (str): Correo electrónico para notificaciones o facturación.
    """
    documento: str
    nombre: str
    telefono: str
    email: str
