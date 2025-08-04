import os
from distancia_geografica import calcular_distancia, calcular_distancia_manhattan, calcular_distancia_manhattan_locais
from population import load_locais_csv
from local import Local

def test_distancia_zero():
    assert calcular_distancia(0, 0, 0, 0) == 0
    assert calcular_distancia_manhattan(0, 0, 0, 0) == 0

def test_distancia_entre_dois_locais_conhecidos():
    # Fórum Eleitoral de Porto Velho/RO: -8.770841339543034, -63.9049906945553    
    # CANTO DO UIRAPURU - ESCOLA MUNICIPAL: -8.8037675,-63.8611508
    # 6.0526 km -> https://www.sunearthtools.com/pt/tools/distance.php
    d = calcular_distancia(-8.770841339543034, -63.9049906945553, -8.8037675, -63.8611508)
    assert 5 < d < 7  # Valor aproximado em km

    # CANTO DO UIRAPURU - ESCOLA MUNICIPAL: -8.8037675,-63.8611508
    # 8.8 Km -> https://www.google.com.br/maps/dir/F%C3%B3rum+Eleitoral+de+Porto+Velho+-+Rua+Jacy+Paran%C3%A1+-+Mato+Grosso,+Porto+Velho+-+RO/EMEI+Canto+do+Uirapuru+-+Rua+Rio+Bonito+-+Aeroclube,+Porto+Velho+-+RO/@-8.786764,-63.8809087,15z/data=!4m14!4m13!1m5!1m1!1s0x92325ce72c269749:0x2b63c2d282928914!2m2!1d-63.9049984!2d-8.7708839!1m5!1m1!1s0x92325b8ae29eb9d5:0xc4b918b228fd99e3!2m2!1d-63.8610448!2d-8.803818!3e0?hl=pt-BR&entry=ttu&g_ep=EgoyMDI1MDcyMy4wIKXMDSoASAFQAw%3D%3D
    d = calcular_distancia_manhattan(-8.770841339543034, -63.9049906945553, -8.8037675,-63.8611508)
    assert 7 < d < 9  # Valor aproximado em km

print(calcular_distancia(-8.770841339543034, -63.9049906945553, -8.8037675,-63.8611508))
print(calcular_distancia_manhattan(-8.770841339543034, -63.9049906945553, -8.8037675, -63.8611508))


# Local inicial padrão (Fórum Eleitoral de Porto Velho/RO)
LOCAL_INICIAL = Local(
    id=0, 
    demanda=0, 
    x=-8.770841339543034, 
    y=-63.9049906945553
)

# filepath_locais = os.path.join(os.path.dirname(__file__), 'data', 'locais-votacao3.csv')
# locais = load_locais_csv(filepath=filepath_locais)
locais = load_locais_csv()

distancia_total = 0
for local in locais:
    distancia = calcular_distancia_manhattan_locais(LOCAL_INICIAL, local)
    distancia_total += distancia
    print(f"Distância {LOCAL_INICIAL.id} -> {local.id}: {distancia:.2f} km")

print(f"Soma das distâncias: {distancia_total:.2f} km")    
