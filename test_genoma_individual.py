from population import gerar_genoma_individual

g = gerar_genoma_individual(max_locais_por_veiculo=3)
g.calcular_fitness()
g.imprimir_status()
g.imprimir_rotas()
