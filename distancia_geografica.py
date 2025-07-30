import math
from typing import List

from local import Local

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


def calcular_distancia_manhattan(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula a distância de Manhattan entre duas coordenadas geográficas (em graus decimais).
    A distância de Manhattan é a soma das diferenças absolutas das coordenadas.
    Retorna a distância em quilômetros.
    """
    raio_terra_km: float = 6371.0
    
    # Converter graus para radianos
    lat1_rad: float = math.radians(lat1)
    lon1_rad: float = math.radians(lon1)
    lat2_rad: float = math.radians(lat2)
    lon2_rad: float = math.radians(lon2)
    
    # Calcular as diferenças absolutas em radianos
    delta_lat_abs: float = abs(lat2_rad - lat1_rad)
    delta_lon_abs: float = abs(lon2_rad - lon1_rad)
    
    # Converter as diferenças angulares para distâncias lineares
    # Para latitude: a distância é diretamente proporcional à diferença angular
    distancia_lat: float = delta_lat_abs * raio_terra_km
    
    # Para longitude: precisa considerar a latitude média para o fator de correção
    lat_media: float = (lat1_rad + lat2_rad) / 2
    distancia_lon: float = delta_lon_abs * raio_terra_km * math.cos(lat_media)
    
    # Distância de Manhattan: soma das componentes
    distancia_manhattan: float = distancia_lat + distancia_lon
    
    return distancia_manhattan

def calcular_distancia_manhattan_locais(local1: Local, local2: Local) -> float:
    return calcular_distancia_manhattan(local1.x, local1.y, local2.x, local2.y)

def calcular_distancia_manhattan_rota(rota: List[Local]) -> float:
    return sum(calcular_distancia_manhattan_locais(rota[i], rota[i+1]) for i in range(len(rota)-1))