from population import generate_random_population, load_locais_csv, load_veiculos_csv
import random
import itertools

POPULATION_SIZE = 500
RANDOM_POPULATION_SIZE = 20
MUTATION_RATE = 0.4
N_GENERATIONS = 5000
ELITE_SIZE = 10  # Quantos melhores manter

veiculos = load_veiculos_csv()
locais = load_locais_csv()
population = generate_random_population(population_size=POPULATION_SIZE, veiculos=veiculos, locais=locais)

best_fitness_values = []
best_solutions = []
# Hereditariedade
# Variação 
# Seleção
for generation in range(N_GENERATIONS):
    print(f"Generation {generation}:")

    # Seleção
    # Calcular fitness para cada indivíduo
    for genoma in population:
        genoma.calcular_fitness()
    fitness_values = [genoma.fitness for genoma in population]
    
    # Selecionar os melhores (elitismo)
    sorted_population = sorted(population, key=lambda g: g.fitness)
    elites = sorted_population[:ELITE_SIZE]
    best_fitness = elites[0].fitness
    best_solution = elites[0]
    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    print(f"Best fitness = {best_fitness:.2f}, Kms = {best_solution.metricas.distancia_percorrida_total:.2f}")    

    # Hereditariedade
    # Seleção dos pais (roleta viciada)
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        selection_probs = [1/POPULATION_SIZE] * POPULATION_SIZE
    else:
        selection_probs = [f/total_fitness for f in fitness_values]

    # adiciona os melhores da geração
    new_population = elites
    # adiciona uma nova população randômica
    new_random_population = generate_random_population(population_size=RANDOM_POPULATION_SIZE, veiculos=veiculos, locais=locais)
    new_population += new_random_population
    # adiciona um cruzamento dos melhores com a nova população randômica
    for parent1 in new_random_population:
        parent2 = random.choice(elites)
        child = parent1.crossover(parceiro=parent2)
        child.mutate(taxa_mutacao=MUTATION_RATE)
        new_population.append(child)
    # Adiciona o restante da população    
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population, weights=selection_probs, k=2)
        # child = random.choice([parent1, parent2])
        child = parent1.crossover(parceiro=parent2)
        child.mutate(taxa_mutacao=MUTATION_RATE)
        new_population.append(child)
    
    population = new_population

print(f"Melhor fitness final: {min(best_fitness_values)}")
best_solution = best_solutions[best_fitness_values.index(min(best_fitness_values))]
best_solution.imprimir_status()
best_solution.imprimir_rotas()
best_solution.imprimir_status_resumido()