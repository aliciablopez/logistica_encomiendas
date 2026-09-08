from abc import ABC, abstractmethod
from models import Cotizacion, Encomienda
from config import TARIFAS_BASE, RECARGOS_SERVICIOS, TASA_IVA


class IEstrategiaCotizacion(ABC):
    """Interfaz para las estrategias de cálculo de costos."""

    @abstractmethod
    def calcular(self, encomienda: Encomienda,
                 cotizacion: Cotizacion) -> Cotizacion:
        pass


class CalculoBaseStrategy(IEstrategiaCotizacion):
    """Calcula el costo base considerando el destino y la categoría de peso."""

    def calcular(self, encomienda: Encomienda,
                 cotizacion: Cotizacion) -> Cotizacion:
        base_zona = TARIFAS_BASE["destinos"].get(encomienda.destino, 1000.0)
        base_peso = TARIFAS_BASE["pesos"].get(encomienda.peso, 500.0)
        cotizacion.subtotal = base_zona + base_peso
        return cotizacion


class RecargosServiciosStrategy(IEstrategiaCotizacion):
    """Calcula los recargos acumulados por servicios adicionales seleccionados."""

    def calcular(self, encomienda: Encomienda,
                 cotizacion: Cotizacion) -> Cotizacion:
        total_recargos = 0.0
        for servicio in encomienda.servicios:
            total_recargos += RECARGOS_SERVICIOS.get(servicio, 0.0)
        cotizacion.recargos = total_recargos
        return cotizacion


class CalculoIvaStrategy(IEstrategiaCotizacion):
    """Calcula el impuesto al valor agregado (IVA) sobre el subtotal y recargos."""

    def calcular(self, encomienda: Encomienda,
                 cotizacion: Cotizacion) -> Cotizacion:
        monto_imponible = cotizacion.subtotal + cotizacion.recargos
        cotizacion.iva = monto_imponible * TASA_IVA
        cotizacion.total = monto_imponible + cotizacion.iva
        return cotizacion


class CotizadorService:
    """Servicio coordinador que ejecuta la cadena de estrategias de cálculo."""

    def __init__(self, estrategias: list[IEstrategiaCotizacion]):
        self.estrategias = estrategias

    def calcular_costo(self, encomienda: Encomienda) -> Cotizacion:
        cotizacion = Cotizacion()
        for estrategia in self.estrategias:
            cotizacion = estrategia.calcular(encomienda, cotizacion)
        return cotizacion