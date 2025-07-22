import math

def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância entre duas coordenadas geográficas (em graus decimais).
    Retorna a distância em quilômetros.
    """
    raio_terra_km: float = 6371.0

    # Converter graus para radianos
    lat1_rad: float = math.radians(lat1)
    lon1_rad: float = math.radians(lon1)
    lat2_rad: float = math.radians(lat2)
    lon2_rad: float = math.radians(lon2)

    # Diferenças
    delta_lat: float = lat2_rad - lat1_rad
    delta_lon: float = lon2_rad - lon1_rad

    # Fórmula de Haversine
    a: float = math.sin(delta_lat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2)**2
    c: float = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distancia: float = raio_terra_km * c
    return distancia
