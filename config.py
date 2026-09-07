# config.py

# ==========================================
# 1. IMPUESTOS Y TASAS GENERALES
# ==========================================
PORCENTAJE_IVA = 0.21         # 21% de IVA
TASA_AEREA_ADICIONAL = 1500.0  # Recargo fijo para envíos aéreos


# ==========================================
# 2. TARIFAS BASE POR TIPO DE SERVICIO
# ==========================================
PRECIOS_SERVICIOS = {
    "ESTANDAR": 1000.0,
    "URGENTE": 2500.0,
    "AEREO": 5000.0,
    "FRAGIL": 1800.0
}


# ==========================================
# 3. RECARGOS POR ZONA DE DESTINO
# ==========================================
RECARGOS_DESTINO = {
    "CABA": 0.0,
    "AMBA": 500.0,
    "CENTRO": 1200.0,
    "COSTA": 1500.0,
    "NORTE": 2000.0,
    "SUR": 2500.0
}


# ==========================================
# 4. RECARGOS POR CATEGORÍA DE PESO
# ==========================================
RECARGOS_PESO = {
    "LIGERO": 0.0,
    "MEDIO": 800.0,
    "PESADO": 1800.0
}