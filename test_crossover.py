import os
from population import gerar_genoma_individual

p1 = gerar_genoma_individual(max_locais_por_veiculo=3)
p1.calcular_fitness()
# p1.imprimir_status()
p1.imprimir_rotas()

p2 = gerar_genoma_individual(max_locais_por_veiculo=3)
p2.calcular_fitness()
# p2.imprimir_status()
p2.imprimir_rotas()

child = p1.crossover(parceiro=p2)
child.calcular_fitness()
child.imprimir_status_resumido()
child.imprimir_rotas()
