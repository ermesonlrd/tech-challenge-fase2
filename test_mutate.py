import os
from population import gerar_genoma_individual

g = gerar_genoma_individual(max_locais_por_veiculo=3)
g.calcular_fitness()
g.imprimir_rotas()
g.imprimir_status_resumido()

g.mutate(taxa_mutacao=0.5)
g.calcular_fitness()
g.imprimir_rotas()
g.imprimir_status_resumido()
