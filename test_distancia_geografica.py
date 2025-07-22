from distancia_geografica import calcular_distancia

def test_distancia_zero():
    assert calcular_distancia(0, 0, 0, 0) == 0

def test_distancia_entre_dois_locais_conhecidos():
    # Fórum Eleitoral de Porto Velho/RO: -8.770841339543034, -63.9049906945553
    # KAWAPU - ESCOLA ESTADUAL - ALDEIA KAWAPU - DISTRITO DE EXTREMA: -9,57522161,-66,3789518    
    # 286.0016 km -> https://www.sunearthtools.com/pt/tools/distance.php
    d = calcular_distancia(-8.7664496, -63.8998567, -9.57522161, -66.3789518)
    assert 280 < d < 290  # Valor aproximado em km

print(calcular_distancia(-8.770841339543034,-63.9049906945553, -9.7778146, -66.3561228))
