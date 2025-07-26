import random
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass

from local import Local
from veiculo import Veiculo
from distancia_geografica import calcular_distancia_manhattan


@dataclass
class MetricasGenoma:
    """Classe para armazenar métricas do genoma"""
    demanda_pendente: Dict[int, int]
    demanda_total: int
    capacidade_ociosa: Dict[int, int]
    capacidade_total: int
    distancia_percorrida: Dict[int, float]
    distancia_percorrida_total: float
    demanda_pendente_total: int
    capacidade_ociosa_total: int


class Genoma:
    """
    Representa um genoma para problema de Vehicle Routing Problem (VRP).
    Cada genoma contém rotas para veículos e métricas de desempenho.
    """
    
    # Constantes para cálculo de fitness
    PENALIDADE_DEMANDA = 200.0
    PENALIDADE_CAPACIDADE = 10.0
    
    # Local inicial padrão (Fórum Eleitoral de Porto Velho/RO)
    LOCAL_INICIAL_PADRAO = Local(
        id=0, 
        demanda=0, 
        x=-8.770841339543034, 
        y=-63.9049906945553
    )

    def __init__(
        self, 
        routes: Dict[Veiculo, List[Local]], 
        local_inicial: Optional[Local] = None, 
        fitness: float = 0.0
    ):
        self.routes = routes
        self.local_inicial = local_inicial or self.LOCAL_INICIAL_PADRAO
        self.fitness = fitness
        
        # Inicializa e calcula métricas
        self.metricas = self._inicializar_metricas()
        self._processar_rotas()

    def _inicializar_metricas(self) -> MetricasGenoma:
        """Inicializa todas as métricas do genoma"""
        locais_unicos = self._obter_locais_unicos()
        veiculos = self.routes.keys()
        
        # Inicializar demandas
        demanda_pendente = {local.id: local.demanda for local in locais_unicos}
        demanda_total = sum(demanda_pendente.values())
        
        # Inicializar capacidades
        capacidade_ociosa = {veiculo.id: veiculo.capacidade for veiculo in veiculos}
        capacidade_total = sum(capacidade_ociosa.values())
        
        # Inicializar distâncias
        distancia_percorrida = {veiculo.id: 0.0 for veiculo in veiculos}
        
        return MetricasGenoma(
            demanda_pendente=demanda_pendente,
            demanda_total=demanda_total,
            capacidade_ociosa=capacidade_ociosa,
            capacidade_total=capacidade_total,
            distancia_percorrida=distancia_percorrida,
            distancia_percorrida_total=0.0,
            demanda_pendente_total=demanda_total,
            capacidade_ociosa_total=capacidade_total
        )

    def _obter_locais_unicos(self) -> Set[Local]:
        """Retorna conjunto de locais únicos presentes nas rotas"""
        locais_unicos = set()
        for route in self.routes.values():
            locais_unicos.update(route)
        return locais_unicos

    def _processar_rotas(self) -> None:
        """Processa todas as rotas calculando distâncias e atendendo demandas"""
        for veiculo, rota in self.routes.items():
            if not rota:
                continue
            
            self._processar_rota_veiculo(veiculo, rota)
        
        self._finalizar_metricas()

    def _processar_rota_veiculo(self, veiculo: Veiculo, rota: List[Local]) -> None:
        """Processa uma rota específica de um veículo"""
        # Distância do local inicial ao primeiro local
        distancia_inicial = calcular_distancia_manhattan(
            self.local_inicial.x, self.local_inicial.y,
            rota[0].x, rota[0].y
        )
        self.metricas.distancia_percorrida[veiculo.id] = distancia_inicial
        self._atender_demanda(veiculo, rota[0])

        # Processar resto da rota
        for i in range(len(rota) - 1):
            local_atual = rota[i]
            proximo_local = rota[i + 1]
            
            distancia_segmento = calcular_distancia_manhattan(
                local_atual.x, local_atual.y,
                proximo_local.x, proximo_local.y
            )
            
            self.metricas.distancia_percorrida[veiculo.id] += distancia_segmento
            self._atender_demanda(veiculo, proximo_local)

    def _atender_demanda(self, veiculo: Veiculo, local: Local) -> None:
        """Atende a demanda de um local com um veículo específico"""
        capacidade_disponivel = self.metricas.capacidade_ociosa[veiculo.id]
        demanda_local = self.metricas.demanda_pendente[local.id]
        
        if capacidade_disponivel <= 0 or demanda_local <= 0:
            return
        
        demanda_atendida = min(capacidade_disponivel, demanda_local)
        
        self.metricas.capacidade_ociosa[veiculo.id] -= demanda_atendida
        self.metricas.demanda_pendente[local.id] -= demanda_atendida

    def _finalizar_metricas(self) -> None:
        """Finaliza o cálculo das métricas totais"""
        self.metricas.distancia_percorrida_total = sum(
            self.metricas.distancia_percorrida.values()
        )
        self.metricas.demanda_pendente_total = sum(
            self.metricas.demanda_pendente.values()
        )
        self.metricas.capacidade_ociosa_total = sum(
            self.metricas.capacidade_ociosa.values()
        )

    def calcular_fitness(self) -> float:
        """Calcula e retorna o fitness do genoma"""
        fitness = (
            self.metricas.distancia_percorrida_total +
            (self.metricas.demanda_pendente_total * self.PENALIDADE_DEMANDA) +
            (self.metricas.capacidade_ociosa_total * self.PENALIDADE_CAPACIDADE)
        )
        
        self.fitness = fitness
        return fitness

    def crossover(self, parceiro: 'Genoma') -> 'Genoma':
        """
        Realiza crossover entre dois genomas
        
        Args:
            parceiro: Outro genoma para crossover
            
        Returns:
            Novo genoma resultante do crossover
        """
        veiculos_combinados = set(self.routes.keys()) | set(parceiro.routes.keys())
        rotas_filho = {}
        
        for veiculo in veiculos_combinados:
            rota_self = self.routes.get(veiculo, [])
            rota_parceiro = parceiro.routes.get(veiculo, [])
            
            rotas_filho[veiculo] = self._combinar_rotas(rota_self, rota_parceiro)
        
        return Genoma(
            routes=rotas_filho,
            local_inicial=self.local_inicial
        )

    def _combinar_rotas(self, rota1: List[Local], rota2: List[Local]) -> List[Local]:
        """Combina duas rotas"""
        if not rota1:
            return rota2.copy()
        if not rota2:
            return rota1.copy()
        
        # Combinar e remover duplicatas mantendo ordem
        locais_combinados = rota1 + rota2
        locais_unicos = self._remover_duplicatas_mantendo_ordem(locais_combinados)
        
        # Embaralhar e ajustar tamanho
        random.shuffle(locais_unicos)
        tamanho_alvo = (len(rota1) + len(rota2)) // 2
        
        return locais_unicos[:tamanho_alvo] if len(locais_unicos) > tamanho_alvo else locais_unicos

    def _remover_duplicatas_mantendo_ordem(self, locais: List[Local]) -> List[Local]:
        """Remove duplicatas mantendo a ordem original"""
        vistos = set()
        resultado = []
        
        for local in locais:
            if local.id not in vistos:
                vistos.add(local.id)
                resultado.append(local)
        
        return resultado

    def mutate(self, taxa_mutacao: float) -> bool:
        """
        Aplica mutação nas rotas do genoma
        
        Args:
            taxa_mutacao: Taxa de mutação (0.0 a 1.0)
            
        Returns:
            True se alguma mutação foi aplicada
        """
        mutacao_aplicada = False
        
        # Mutação 1: Trocar posições em rotas existentes
        if self._mutar_trocar_posicoes(taxa_mutacao):
            mutacao_aplicada = True
        
        # Mutação 2: Mover locais entre veículos
        if self._mutar_mover_entre_veiculos(taxa_mutacao):
            mutacao_aplicada = True

        # Mutação 3: Remover locais excedentes e redistribuir
        if self._mutar_remover_excedentes(taxa_mutacao):
            mutacao_aplicada = True    
        
        # Recalcular métricas se houve mutação
        if mutacao_aplicada:
            self.metricas = self._inicializar_metricas()
            self._processar_rotas()
        
        return mutacao_aplicada

    def _mutar_trocar_posicoes(self, taxa_mutacao: float) -> bool:
        """Troca posições de locais dentro das rotas"""
        mutacao_aplicada = False
        
        for rota in self.routes.values():
            if random.random() < taxa_mutacao and len(rota) >= 2:
                i, j = random.sample(range(len(rota)), 2)
                rota[i], rota[j] = rota[j], rota[i]
                mutacao_aplicada = True
        
        return mutacao_aplicada

    def _mutar_mover_entre_veiculos(self, taxa_mutacao: float) -> bool:
        """Move locais entre diferentes veículos"""
        if random.random() >= taxa_mutacao or len(self.routes) <= 1:
            return False
        
        veiculos = list(self.routes.keys())
        if len(veiculos) < 2:
            return False
        
        veiculo_origem, veiculo_destino = random.sample(veiculos, 2)
        rota_origem = self.routes[veiculo_origem]
        rota_destino = self.routes[veiculo_destino]
        
        if not rota_origem:
            return False
        
        # Mover local aleatório
        local_movido = random.choice(rota_origem)
        rota_origem.remove(local_movido)

        if local_movido in rota_destino:
            return True  # já existe na rota de destino, não move, apenas remove da origem
        
        posicao_insercao = random.randint(0, len(rota_destino))
        rota_destino.insert(posicao_insercao, local_movido)
        
        return True

    def _mutar_remover_excedentes(self, taxa_mutacao: float) -> bool:
        """Remove locais excedentes de rotas sobrecarregadas e redistribui"""
        if random.random() >= taxa_mutacao:
            return False
        
        mutacao_aplicada = False
        locais_removidos = []
        
        # Identifica rotas com demanda excedente e remove últimos locais
        for veiculo, rota in self.routes.items():
            if not rota:
                continue
            
            demanda_rota = sum(local.demanda for local in rota)
            
            # Se demanda excede capacidade, remove últimos locais
            if demanda_rota > veiculo.capacidade:
                locais_a_remover = []
                demanda_acumulada = 0
                
                # Remove locais do final até que a demanda seja <= capacidade
                for i in range(len(rota) - 1, -1, -1):
                    local = rota[i]
                    demanda_acumulada += local.demanda
                    locais_a_remover.append(local)
                    
                    # Para quando a demanda restante cabe na capacidade
                    if (demanda_rota - demanda_acumulada) <= veiculo.capacidade:
                        break
                
                # Remove os locais identificados
                for local in locais_a_remover:
                    rota.remove(local)
                    mutacao_aplicada = True
                
                # Adiciona à lista de locais para redistribuir
                locais_removidos.extend(locais_a_remover)
        
        # Redistribui locais removidos que não estão em outras rotas
        if locais_removidos:
            self._redistribuir_locais_removidos(locais_removidos)
        
        return mutacao_aplicada
    
    def _redistribuir_locais_removidos(self, locais_removidos: List[Local]) -> None:
        """Redistribui locais removidos para outras rotas"""
        # Identifica todos os locais presentes nas rotas atuais
        locais_nas_rotas = set()
        for rota in self.routes.values():
            for local in rota:
                locais_nas_rotas.add(local.id)
        
        # Filtra locais que realmente precisam ser redistribuídos
        locais_para_redistribuir = [
            local for local in locais_removidos 
            if local.id not in locais_nas_rotas
        ]
        
        if not locais_para_redistribuir:
            return
        
        # Obter lista de veículos disponíveis
        veiculos_disponiveis = list(self.routes.keys())
        
        if not veiculos_disponiveis:
            return
        
        # Redistribui cada local para um veículo aleatório
        for local in locais_para_redistribuir:
            veiculo_destino = random.choice(veiculos_disponiveis)
            rota_destino = self.routes[veiculo_destino]
            
            # Adiciona em posição aleatória
            if rota_destino:
                posicao = random.randint(0, len(rota_destino))
            else:
                posicao = 0
            
            rota_destino.insert(posicao, local)    

    def imprimir_status(self) -> None:
        """Imprime status detalhado do genoma"""
        self._imprimir_status_demandas()
        self._imprimir_status_veiculos()
        self._imprimir_fitness()

    def _imprimir_status_demandas(self) -> None:
        """Imprime status das demandas dos locais"""
        print("\n=== STATUS DAS DEMANDAS DOS LOCAIS ===")
        print(f"Demanda Total: {self.metricas.demanda_total}")
        
        locais_unicos = self._obter_locais_unicos()
        for local in sorted(locais_unicos, key=lambda l: l.id):
            pendente = self.metricas.demanda_pendente[local.id]
            status = "✓" if pendente <= 0 else "✗"
            print(f"Local {local.id}: Demanda {local.demanda}, Pendente {pendente} {status}")

    def _imprimir_status_veiculos(self) -> None:
        """Imprime status dos veículos"""
        print("\n=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===")
        print(f"Capacidade Total: {self.metricas.capacidade_total}")
        print(f"Distância Total: {self.metricas.distancia_percorrida_total:.2f} km")
        
        for veiculo in sorted(self.routes.keys(), key=lambda v: v.id):
            ociosa = self.metricas.capacidade_ociosa[veiculo.id]
            distancia = self.metricas.distancia_percorrida[veiculo.id]
            status = "✓" if ociosa <= 0 else "✗"
            print(f"Veículo {veiculo.id}: Capacidade {veiculo.capacidade}, "
                  f"Ociosa {ociosa} {status}, Distância {distancia:.2f} km")

    def _imprimir_fitness(self) -> None:
        """Imprime informações de fitness"""
        print("\n=== FITNESS ===")
        print(f"Fitness: {self.fitness:.2f}")

    def imprimir_rotas(self) -> None:
        """Imprime as rotas do genoma de forma organizada"""
        print("\n=== ROTAS DO GENOMA ===")
        
        for veiculo in sorted(self.routes.keys(), key=lambda v: v.id):
            rota = self.routes[veiculo]
            locais_str = ", ".join([f"L{local.id} ({local.demanda})" for local in rota])
            
            print(f"V{veiculo.id} {veiculo.modelo} {veiculo.ano} "
                  f"({veiculo.capacidade}): [{locais_str}]")

    def obter_locais_unicos(self) -> Set[Local]:
        """Retorna conjunto de locais únicos (método público)"""
        return self._obter_locais_unicos()

    def obter_resumo_metricas(self) -> Dict[str, float]:
        """Retorna resumo das principais métricas"""
        return {
            'distancia_total': self.metricas.distancia_percorrida_total,
            'demanda_pendente_total': self.metricas.demanda_pendente_total,
            'capacidade_ociosa_total': self.metricas.capacidade_ociosa_total,
            'fitness': self.fitness,
            'taxa_atendimento': 1 - (self.metricas.demanda_pendente_total / self.metricas.demanda_total) if self.metricas.demanda_total > 0 else 1.0
        }