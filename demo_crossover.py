#!/usr/bin/env python3
"""
Demonstração detalhada do método crossover
"""

from genoma import Genoma
from local import Local
from veiculo import Veiculo

def create_demo_genomes():
    """Cria genomas de demonstração com rotas mais complexas"""
    
    # Cria veículos
    v1 = Veiculo(id=1, capacidade=10, ano='2020', modelo='HILUX')
    v2 = Veiculo(id=2, capacidade=8, ano='2021', modelo='S10')
    v3 = Veiculo(id=3, capacidade=12, ano='2019', modelo='RANGER')
    
    # Cria locais
    l0 = Local(id=0, demanda=0, x=-8.770841, y=-63.904990)  # ponto inicial
    l1 = Local(id=1, demanda=5, x=-8.7924375, y=-63.8936077)
    l2 = Local(id=2, demanda=3, x=-8.7868066, y=-63.8967103)
    l3 = Local(id=3, demanda=2, x=-8.7643882, y=-63.8881511)
    l4 = Local(id=4, demanda=4, x=-8.7543882, y=-63.8781511)
    l5 = Local(id=5, demanda=1, x=-8.7443882, y=-63.8681511)
    l6 = Local(id=6, demanda=6, x=-8.7343882, y=-63.8581511)
    l7 = Local(id=7, demanda=3, x=-8.7243882, y=-63.8481511)
    
    # Genoma Pai 1: Rotas mais longas
    routes1 = {
        v1: [l1, l2, l3],  # 3 locais
        v2: [l4, l5],      # 2 locais
        v3: []             # Rota vazia
    }
    
    # Genoma Pai 2: Rotas diferentes
    routes2 = {
        v1: [l6],          # 1 local
        v2: [],            # Rota vazia
        v3: [l7, l1, l4]   # 3 locais
    }
    
    g1 = Genoma(routes=routes1, local_inicial=l0)
    g2 = Genoma(routes=routes2, local_inicial=l0)
    
    return g1, g2

def print_genome_details(genome, name):
    """Imprime detalhes de um genoma"""
    print(f"\n{name}:")
    print(f"  Local inicial: {genome.local_inicial.id}")
    print(f"  Número de veículos: {len(genome.routes)}")
    
    total_locations = 0
    for v, route in genome.routes.items():
        print(f"  Veículo {v.id} ({v.modelo}): {[l.id for l in route]} ({len(route)} locais)")
        total_locations += len(route)
    
    print(f"  Total de locais visitados: {total_locations}")
    
    # Calcula fitness
    fitness = genome.calc_fitness()
    print(f"  Fitness: {fitness:.2f}")

def demo_crossover_process():
    """Demonstra o processo completo de crossover"""
    
    print("=" * 60)
    print("DEMONSTRAÇÃO DO MÉTODO CROSSOVER")
    print("=" * 60)
    
    # Cria os genomas pais
    g1, g2 = create_demo_genomes()
    
    # Mostra detalhes dos pais
    print_genome_details(g1, "GENOMA PAI 1")
    print_genome_details(g2, "GENOMA PAI 2")
    
    # Realiza o crossover
    print("\n" + "=" * 40)
    print("REALIZANDO CROSSOVER...")
    print("=" * 40)
    
    child = g1.crossover(g2)
    
    # Mostra detalhes do filho
    print_genome_details(child, "GENOMA FILHO")
    
    # Análise do resultado
    print("\n" + "=" * 40)
    print("ANÁLISE DO RESULTADO")
    print("=" * 40)
    
    # Verifica quais veículos foram herdados
    print("Veículos dos pais:")
    print(f"  Pai 1: {[v.id for v in g1.routes.keys()]}")
    print(f"  Pai 2: {[v.id for v in g2.routes.keys()]}")
    print(f"  Filho:  {[v.id for v in child.routes.keys()]}")
    
    # Verifica se todos os veículos dos pais estão no filho
    all_parent_vehicles = set(g1.routes.keys()) | set(g2.routes.keys())
    child_vehicles = set(child.routes.keys())
    
    if child_vehicles == all_parent_vehicles:
        print("✅ Todos os veículos dos pais estão presentes no filho")
    else:
        print("❌ Alguns veículos dos pais não estão no filho")
    
    # Verifica se o local inicial foi preservado
    if child.local_inicial.id == g1.local_inicial.id:
        print("✅ Local inicial foi preservado")
    else:
        print("❌ Local inicial não foi preservado")
    
    # Mostra como as rotas foram combinadas
    print("\nCombinação das rotas:")
    for v in all_parent_vehicles:
        route1 = g1.routes.get(v, [])
        route2 = g2.routes.get(v, [])
        child_route = child.routes.get(v, [])
        
        print(f"  Veículo {v.id}:")
        print(f"    Pai 1: {[l.id for l in route1]}")
        print(f"    Pai 2: {[l.id for l in route2]}")
        print(f"    Filho:  {[l.id for l in child_route]}")
    
    return child

def demo_multiple_crossovers():
    """Demonstra múltiplos crossovers para mostrar a aleatoriedade"""
    
    print("\n" + "=" * 60)
    print("DEMONSTRAÇÃO DE MÚLTIPLOS CROSSOVERS")
    print("=" * 60)
    
    g1, g2 = create_demo_genomes()
    
    print("Realizando 5 crossovers diferentes:")
    
    children = []
    for i in range(5):
        child = g1.crossover(g2)
        children.append(child)
        
        print(f"\nCrossover {i+1}:")
        for v, route in child.routes.items():
            print(f"  V{v.id}: {[l.id for l in route]}")
    
    # Verifica a diversidade dos resultados
    unique_results = set()
    for child in children:
        # Cria uma representação única do genoma
        genome_repr = tuple(sorted([(v.id, tuple(l.id for l in route)) for v, route in child.routes.items()]))
        unique_results.add(genome_repr)
    
    print(f"\nDiversidade dos resultados:")
    print(f"  Número de resultados únicos: {len(unique_results)} de 5")
    print(f"  Taxa de diversidade: {len(unique_results)/5*100:.1f}%")
    
    if len(unique_results) > 1:
        print("✅ O crossover produz resultados diversos devido à aleatoriedade")
    else:
        print("⚠️  Todos os resultados foram iguais (pode ser coincidência)")

if __name__ == "__main__":
    try:
        # Demonstração principal
        child = demo_crossover_process()
        
        # Demonstração de múltiplos crossovers
        demo_multiple_crossovers()
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro na demonstração: {e}")
        import traceback
        traceback.print_exc() 