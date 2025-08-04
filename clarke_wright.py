from typing import Dict, List, Tuple
from itertools import combinations

from local import Local
from veiculo import Veiculo
from distancia_geografica import calcular_distancia_manhattan_locais


def clarke_wright(locais: List[Local], veiculos: List[Veiculo], deposito: Local) -> Dict[Veiculo, List[Local]]:
    # Ignora o depósito na lista de clientes
    clientes = [l for l in locais if l.id != deposito.id]

    # Rota inicial: um veículo por cliente
    rotas: Dict[int, List[Local]] = {cliente.id: [deposito, cliente, deposito] for cliente in clientes}
    demandas: Dict[int, int] = {cliente.id: cliente.demanda for cliente in clientes}

    # Cálculo das economias
    savings: List[Tuple[float, int, int]] = []
    for i, j in combinations(clientes, 2):
        s = calcular_distancia_manhattan_locais(deposito, i) + calcular_distancia_manhattan_locais(deposito, j) - calcular_distancia_manhattan_locais(i, j)
        savings.append((s, i.id, j.id))
    savings.sort(reverse=True)

    # Processamento das economias
    for _, i_id, j_id in savings:
        # Verifica se i e j ainda estão em rotas diferentes
        rotas_i = next((rid for rid, r in rotas.items() if any(loc.id == i_id for loc in r[1:-1])), None)
        rotas_j = next((rid for rid, r in rotas.items() if any(loc.id == j_id for loc in r[1:-1])), None)

        if rotas_i is None or rotas_j is None or rotas_i == rotas_j:
            continue

        r1 = rotas[rotas_i]
        r2 = rotas[rotas_j]

        # Verifica se é possível unir as rotas respeitando as condições de extremidade
        if r1[-2].id == i_id and r2[1].id == j_id:
            nova_rota = r1[:-1] + r2[1:]
        elif r2[-2].id == j_id and r1[1].id == i_id:
            nova_rota = r2[:-1] + r1[1:]
        else:
            continue

        demanda_total = demandas[rotas_i] + demandas[rotas_j]
        if demanda_total <= max(v.capacidade for v in veiculos):
            # Atualiza rotas e demandas
            novo_id = max(rotas.keys()) + 1
            rotas[novo_id] = nova_rota
            demandas[novo_id] = demanda_total
            del rotas[rotas_i]
            del rotas[rotas_j]
            del demandas[rotas_i]
            del demandas[rotas_j]

    # Atribuição dos veículos disponíveis às rotas geradas
    rotas_finais: Dict[Veiculo, List[Local]] = {}
    for rota, demanda in zip(rotas.values(), demandas.values()):        
        veiculos_disponiveis = [v for v in veiculos if v not in rotas_finais]
        veiculo_disponivel = next((v for v in veiculos_disponiveis if v.capacidade >= demanda), None)

        if veiculo_disponivel:
            rotas_finais[veiculo_disponivel] = rota
        else:
            raise Exception(f"Não há veículo disponível com capacidade suficiente para demanda {demanda}.")


    return rotas_finais
