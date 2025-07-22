from population import gerar_genoma_individual

g = gerar_genoma_individual(max_locais_por_veiculo=3)
g.calc_fitness()
g.print_routes()
g.print_status()