import random
from typing import Dict, List, Optional

from local import Local
from veiculo import Veiculo
from distancia_geografica import calcular_distancia

class Genoma:
    def __init__(self, routes: Dict[Veiculo, List[Local]], local_inicial: Optional[Local] = None, fitness: float = 0.0):
        self.routes = routes  # Lista de rotas, onde cada rota é uma lista de locais atendidos por um veículo
        self.local_inicial = local_inicial if local_inicial is not None else self.__local_inicial_padrao()  # Local de partida
        self.fitness = fitness        
        
        self._reset()
        self.percorrer_rotas()        

    def _reset(self):
        """Reseta os atributos de demanda e capacidade"""
        # Atributos para calculo de demandas dos locais
        self.demanda_pendente = self._inicializar_demanda_pendente()
        self.demanda_total = sum(self.demanda_pendente.values())
        # Atributos para calculos de capacidade dos veiculos e distancia percorrida
        self.capacidade_ociosa = self._inicializar_capacidade_ociosa()
        self.capacidade_total = sum(self.capacidade_ociosa.values())
        # {veiculo.id -> distancia_percorrida}
        self.distancia_percorrida = {}

    def _inicializar_demanda_pendente(self):
        """Inicializa o dicionário de demanda pendente no formato {local.id -> local.demanda}"""
        demanda_pendente = {}
        
        # Coleta todos os locais únicos das rotas
        locais_unicos = set()
        for route in self.routes.values():
            for local in route:
                locais_unicos.add(local)
        
        # Inicializa a demanda pendente para cada local
        for local in locais_unicos:
            demanda_pendente[local.id] = local.demanda
            
        return demanda_pendente

    def _inicializar_capacidade_ociosa(self):
        """Inicializa o dicionário de capacidade ociosa no formato {veiculo.id -> veiculo.capacidade}"""
        capacidade_ociosa = {}
        
        # Coleta todos os veículos das rotas
        for veiculo in self.routes.keys():
            capacidade_ociosa[veiculo.id] = veiculo.capacidade
            
        return capacidade_ociosa

    def percorrer_rotas(self):
        """Calcula a distância percorrida pelos veículos"""        
        for veiculo, route in self.routes.items():
            if not route:
                continue
            # Distância do local_inicial até o primeiro local da rota
            self.distancia_percorrida[veiculo.id] = calcular_distancia(self.local_inicial.x, self.local_inicial.y, route[0].x, route[0].y)
            self.atender_demanda(veiculo=veiculo, local=route[0])

            # Distância entre os locais subsequentes
            for i in range(len(route) - 1):
                local_a = route[i]
                local_b = route[i + 1]
                self.distancia_percorrida[veiculo.id] += calcular_distancia(local_a.x, local_a.y, local_b.x, local_b.y)
                self.atender_demanda(veiculo=veiculo, local=local_b)
        self.distancia_percorrida_total = sum(self.distancia_percorrida.values())
        self.demanda_pendente_total = sum(self.demanda_pendente.values())
        self.capacidade_ociosa_total = sum(self.capacidade_ociosa.values())

    def __local_inicial_padrao(self):
        # Fórum Eleitoral de Porto Velho/RO
        # -8.770841339543034, -63.9049906945553
        return Local(id=0, demanda=0, x=-8.770841339543034, y=-63.9049906945553)

    def atender_demanda(self, veiculo: Veiculo, local: Local):   
        if self.capacidade_ociosa[veiculo.id] <= 0 or  self.demanda_pendente[local.id] <= 0:
            return
        # Se a capacidade do veículo é maior que a demanda do local, atende a demanda do local
        if self.capacidade_ociosa[veiculo.id] >= self.demanda_pendente[local.id]:
           self.capacidade_ociosa[veiculo.id] -= self.demanda_pendente[local.id]
           self.demanda_pendente[local.id] = 0
        # Se a demanda do local é maior que a capacidade do veículo
        else:
            self.demanda_pendente[local.id] -= self.capacidade_ociosa[veiculo.id]
            self.capacidade_ociosa[veiculo.id] = 0
        

    def print_status(self):
        """Imprime o status do genoma"""
        print("\n=== STATUS DAS DEMANDAS DOS LOCAIS ===")
        print(f"Demanda Total: {self.demanda_total}")
        # Considera apenas locais únicos
        locais_unicos = set()
        for route in self.routes.values():
            for local in route:
                locais_unicos.add(local)
        
        for local in locais_unicos:
            pendente = self.demanda_pendente[local.id]
            status = "✓" if pendente <= 0 else "✗"
            print(f"Local {local.id}: Demanda {local.demanda}, Pendente {pendente} {status}")
        
        print("\n=== STATUS DAS CAPACIDADES E DISTÂNCIAS PERCORRIDAS DOS VEÍCULOS ===")
        print(f"Capacidade Total: {self.capacidade_total}")
        print(f"Distância Total: {self.distancia_percorrida_total}")
        
        for veiculo in self.routes.keys():
            ociosa = self.capacidade_ociosa[veiculo.id]
            status = "✓" if ociosa <= 0 else "✗"
            print(f"Veículo {veiculo.id}: Capacidade {veiculo.capacidade}, Ociosa {ociosa} {status}, Distância {self.distancia_percorrida[veiculo.id]:.2f} km")
        print("\n=== FITNESS ===")
        print(f"Fitness: {self.fitness:.2f}")

    def print_routes(self):
        """Imprime as rotas do genoma"""
        print("\n=== ROTAS DO GENOMA ===")
        
        for veiculo in self.routes.keys():            
            # Formata os locais da rota: L1, L2, L3, ...
            locais_str = ", ".join([f"L{local.id} ({local.demanda})" for local in self.routes[veiculo]])
            
            # Imprime no formato solicitado: V1 {modelo} {ano} ({capacidade}): [L{numero}, L{numero}]
            print(f"V{veiculo.id} {veiculo.modelo} {veiculo.ano} ({veiculo.capacidade}): [{locais_str}]")        

    def calc_fitness(self):        
        # Penalidades: demanda não atendida tem peso muito maior
        PENALIDADE_DEMANDA = 200.0  # Penalidade alta para demanda não atendida
        PENALIDADE_CAPACIDADE = 10.0  # Penalidade menor para capacidade não utilizada
        
        # Fitness é a distância total + penalidades
        self.fitness = self.distancia_percorrida_total + (self.demanda_pendente_total * PENALIDADE_DEMANDA) + (self.capacidade_ociosa_total * PENALIDADE_CAPACIDADE)
        return self.fitness

    def crossover(self, partner: 'Genoma') -> 'Genoma':
        """
        Realiza o crossover entre dois genomas, combinando suas rotas de forma randômica e equitativa.
        
        Args:
            partner: Outro genoma para realizar o crossover
            
        Returns:
            Novo genoma resultante da combinação
        """
        # Obtém todos os veículos únicos dos dois genomas
        all_vehicles = set(self.routes.keys()) | set(partner.routes.keys())
        child_routes = {}
        
        for vehicle in all_vehicles:
            # Verifica se o veículo existe em ambos os genomas
            self_route = self.routes.get(vehicle, [])
            partner_route = partner.routes.get(vehicle, [])
            
            if not self_route and not partner_route:
                # Veículo não existe em nenhum dos genomas
                continue
            elif not self_route:
                # Veículo só existe no partner
                child_routes[vehicle] = partner_route.copy()
            elif not partner_route:
                # Veículo só existe no self
                child_routes[vehicle] = self_route.copy()
            else:
                # Veículo existe em ambos - combina as rotas
                child_routes[vehicle] = self._combine_routes(self_route, partner_route)
        
        # Usa o local_inicial do primeiro genoma (pode ser aleatório também)
        local_inicial = self.local_inicial
        
        # Cria o novo genoma
        child = Genoma(routes=child_routes, local_inicial=local_inicial)
        
        return child
    
    def _combine_routes(self, route1: List[Local], route2: List[Local]) -> List[Local]:
        """
        Combina duas rotas de forma randômica e equitativa.
        
        Args:
            route1: Primeira rota
            route2: Segunda rota
            
        Returns:
            Nova rota combinada
        """
        if not route1:
            return route2.copy()
        if not route2:
            return route1.copy()
        
        # Combina os locais das duas rotas
        all_locals = route1 + route2
        
        # Remove duplicatas mantendo a ordem
        seen = set()
        unique_locals = []
        for local in all_locals:
            if local.id not in seen:
                seen.add(local.id)
                unique_locals.append(local)
        
        # Embaralha a lista de locais únicos
        random.shuffle(unique_locals)
        
        # Decide o tamanho da nova rota (média dos tamanhos originais)
        target_length = (len(route1) + len(route2)) // 2
        
        # Ajusta o tamanho se necessário
        if len(unique_locals) > target_length:
            unique_locals = unique_locals[:target_length]
        
        return unique_locals

    # def mutate(self, mutation_rate: float):
    #     """
    #     Aplica mutação nas rotas do genoma.
        
    #     Args:
    #         mutation_rate: Taxa de mutação (0.0 a 1.0)
    #     """
    #     mutation_applied = False
        
    #     # Primeiro, calcula o fitness para ter os dados de demanda atendida atualizados
    #     self.calc_fitness()
        
    #     # Coleta todos os locais únicos e suas demandas atendidas
    #     locais_unicos = set()
    #     for route in self.routes.values():
    #         for local in route:
    #             locais_unicos.add(local)
        
    #     # Identifica locais com demanda não atendida
    #     locais_demanda_nao_atendida = []
    #     for local in locais_unicos:
    #         if local.demanda_atendida < local.demanda:
    #             # Adiciona o local múltiplas vezes baseado na demanda não atendida
    #             for _ in range(local.demanda - local.demanda_atendida):
    #                 locais_demanda_nao_atendida.append(local)
        
    #     # Identifica veículos com capacidade disponível
    #     veiculos_capacidade_disponivel = []
    #     for veiculo in self.routes.keys():
    #         capacidade_disponivel = veiculo.capacidade - veiculo.capacidade_atendida
    #         if capacidade_disponivel > 0:
    #             veiculos_capacidade_disponivel.append((veiculo, capacidade_disponivel))
        
    #     # Mutação 1: Troca posições em rotas existentes
    #     for vehicle, route in self.routes.items():
    #         if random.random() < mutation_rate and len(route) >= 2:
    #             # Troca dois locais aleatórios na rota
    #             i, j = random.sample(range(len(route)), 2)
    #             route[i], route[j] = route[j], route[i]
    #             mutation_applied = True
        
    #     # Mutação 2: Adiciona locais com demanda não atendida para veículos com capacidade
    #     if random.random() < mutation_rate and locais_demanda_nao_atendida and veiculos_capacidade_disponivel:
    #         # Escolhe um veículo aleatório com capacidade disponível
    #         veiculo, capacidade_disponivel = random.choice(veiculos_capacidade_disponivel)
            
    #         # Escolhe um local aleatório com demanda não atendida
    #         local_para_adicionar = random.choice(locais_demanda_nao_atendida)
            
    #         # Escolhe uma posição aleatória na rota do veículo
    #         posicao = random.randint(0, len(self.routes[veiculo]))
            
    #         # Adiciona o local na posição escolhida
    #         self.routes[veiculo].insert(posicao, local_para_adicionar)
    #         mutation_applied = True
            
    #         # print(f"Mutacao: Adicionado local {local_para_adicionar.id} na posicao {posicao} do veiculo {veiculo.id}")
        
    #     # Mutação 3: Move locais entre veículos (se houver múltiplos veículos)
    #     if random.random() < mutation_rate and len(self.routes) > 1:
    #         # Escolhe dois veículos aleatórios diferentes
    #         veiculos = list(self.routes.keys())
    #         if len(veiculos) >= 2:
    #             veiculo_origem, veiculo_destino = random.sample(veiculos, 2)
                
    #             # Verifica se o veículo origem tem locais e o destino tem capacidade
    #             if (self.routes[veiculo_origem] and 
    #                 veiculo_destino.capacidade_atendida < veiculo_destino.capacidade):
                    
    #                 # Escolhe um local aleatório do veículo origem
    #                 local_movido = random.choice(self.routes[veiculo_origem])
                    
    #                 # Remove do veículo origem
    #                 self.routes[veiculo_origem].remove(local_movido)
                    
    #                 # Adiciona no veículo destino em posição aleatória
    #                 posicao = random.randint(0, len(self.routes[veiculo_destino]))
    #                 self.routes[veiculo_destino].insert(posicao, local_movido)
                    
    #                 mutation_applied = True
    #                 # print(f"Mutacao: Movido local {local_movido.id} do veiculo {veiculo_origem.id} para veiculo {veiculo_destino.id} na posicao {posicao}")
        
    #     # Recalcula a distância total se uma mutação foi aplicada
    #     if mutation_applied:
    #         self._calculate_total_distance()
    #         # print(f"Mutacao aplicada. Nova distancia total: {self._total_distance:.2f}")

    # def print_distances(self):
    #     for v_idx, (veiculo, route) in enumerate(self.routes.items(), 1):
    #         if not route:
    #             continue
    #         # Distância do local_inicial até o primeiro local
    #         dist = calcular_distancia(self.local_inicial.x, self.local_inicial.y, route[0].x, route[0].y)
    #         print(f"V{v_idx}: {self.local_inicial.id} até {route[0].id}: {dist:.2f} km")
    #         # Distâncias entre os locais subsequentes
    #         for i in range(len(route) - 1):
    #             local_a = route[i]
    #             local_b = route[i + 1]
    #             dist = calcular_distancia(local_a.x, local_a.y, local_b.x, local_b.y)
    #             print(f"V{v_idx}: {local_a.id} até {local_b.id}: {dist:.2f} km")
    