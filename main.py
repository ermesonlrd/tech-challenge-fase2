from population import generate_random_population, load_locais_csv, load_veiculos_csv
import random
import itertools

POPULATION_SIZE = 500
RANDOM_POPULATION_SIZE = 50
MUTATION_RATE = 0.2
N_GENERATIONS = 3000
ELITE_SIZE = 6  # Quantos melhores manter

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
        genoma.calc_fitness()
    fitness_values = [genoma.fitness for genoma in population]
    
    # Selecionar os melhores (elitismo)
    sorted_population = sorted(population, key=lambda g: g.fitness)
    elites = sorted_population[:ELITE_SIZE]
    best_fitness = elites[0].fitness
    best_solution = elites[0]
    best_fitness_values.append(best_fitness)
    best_solutions.append(best_solution)

    print(f"Generation {generation}: Best fitness = {best_fitness}")    

    # Hereditariedade
    # Seleção dos pais (roleta viciada)
    total_fitness = sum(fitness_values)
    if total_fitness == 0:
        selection_probs = [1/POPULATION_SIZE] * POPULATION_SIZE
    else:
        selection_probs = [f/total_fitness for f in fitness_values]

    new_population = elites
    new_population += generate_random_population(population_size=RANDOM_POPULATION_SIZE, veiculos=veiculos, locais=locais)
    while len(new_population) < POPULATION_SIZE:
        parent1, parent2 = random.choices(population, weights=selection_probs, k=2)
        child = random.choice([parent1, parent2])
        # child = parent1.crossover(partner=parent2)
        # child.mutate(mutation_rate=MUTATION_RATE)        
        new_population.append(child)

    # population = new_population + generate_random_population(population_size=POPULATION_SIZE - len(new_population))
    population = new_population

print(f"Melhor fitness final: {min(best_fitness_values)}")
best_solution = best_solutions[best_fitness_values.index(min(best_fitness_values))]
best_solution.print_routes()
best_solution.print_status()
