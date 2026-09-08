# ==========================================
# CONFIGURACIÓN CENTRALIZADA DE TARIFAS
# ==========================================

TARIFAS_BASE = {
    "destinos": {
        "CABA": 1500.0,
        "GBA_NORTE": 2000.0,
        "GBA_SUR": 2200.0,
        "INTERIOR": 3500.0
    },
    "pesos": {
        "LIVIANO": 500.0,
        "MEDIO": 1000.0,
        "PESADO": 2000.0
    }
}

RECARGOS_SERVICIOS = {
    "URGENTE": 1200.0,
    "FRAGIL": 800.0,
    "EXPRESS": 1500.0
}

TASA_IVA = 0.21