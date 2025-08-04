import os
from distancia_geografica import calcular_distancia_manhattan_rota
from local import Local
from population import gerar_genoma_individual
from population import load_locais_csv, load_veiculos_csv

# g = gerar_genoma_individual(max_locais_por_veiculo=3)
# g.calcular_fitness()
# g.imprimir_status()
# g.imprimir_rotas()


filepath_veiculos = os.path.join(os.path.dirname(__file__), 'data', 'veiculos3.csv')
veiculos = load_veiculos_csv(filepath=filepath_veiculos)
filepath_locais = os.path.join(os.path.dirname(__file__), 'data', 'locais-votacao3.csv')
locais = load_locais_csv(filepath=filepath_locais)
print(f"Número de veículos: {len(veiculos)}")
print(f"Número de locais: {len(locais)}")
# Local inicial padrão (Fórum Eleitoral de Porto Velho/RO)
LOCAL_INICIAL_PADRAO = Local(
    id=0, 
    demanda=0, 
    x=-8.770841339543034, 
    y=-63.9049906945553
)

g = gerar_genoma_individual(max_locais_por_veiculo=1, veiculos=veiculos, locais=locais, local_inicial=LOCAL_INICIAL_PADRAO)
g.calcular_fitness()
g.imprimir_status()
g.imprimir_rotas()

from clarke_wright import clarke_wright

# Executa o algoritmo
rotas = clarke_wright(locais, veiculos, LOCAL_INICIAL_PADRAO)

# Exibe rotas e distâncias
print("\n\n")
print("======Clarke-Wright (Savings Algorithm)======\n")
for veiculo, rota in rotas.items():
    print(f"Veículo {veiculo.id} – Rota: {[l.id for l in rota]} – Distância total: {calcular_distancia_manhattan_rota(rota)} km")
