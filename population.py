import csv
import os
import random
from veiculo import Veiculo
from local import Local
from genoma import Genoma


def load_veiculos_csv(filepath=None):
    """
    Loads veiculos from CSV file and returns a list of Veiculo objects.
    Each Veiculo is initialized with a unique id, capacidade from 'QUANTIDADE_DE_URNAS', ano from 'ANO', and modelo from 'MODELO'.    
    """
    if filepath is None:
        # Default path relative to this file
        filepath = os.path.join(os.path.dirname(__file__), 'data', 'veiculos.csv')
    veiculos = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for idx, row in enumerate(reader):
            capacidade = int(row['QUANTIDADE_DE_URNAS'])
            ano = row['ANO'].strip()
            modelo = row['MODELO'].strip()
            veiculo = Veiculo(id=idx, capacidade=capacidade, ano=ano, modelo=modelo)
            veiculos.append(veiculo)
    return veiculos


def load_locais_csv(filepath=None):
    """
    Loads locais from CSV file and returns a list of Local objects.
    Each Local is initialized with id (NUMERO), demanda (SECOES_PREVISTAS), x (LATITUDE), and y (LONGITUDE).    
    """
    if filepath is None:
        filepath = os.path.join(os.path.dirname(__file__), 'data', 'locais-votacao.csv')
    locais = []
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                id_ = int(row['NUMERO'])
                demanda = int(row['SECOES_PREVISTAS'])
                x = float(row['LATITUDE'].replace(',', '.')) if row['LATITUDE'] else 0.0
                y = float(row['LONGITUDE'].replace(',', '.')) if row['LONGITUDE'] else 0.0
                local = Local(id=id_, demanda=demanda, x=x, y=y)
                locais.append(local)
            except (ValueError, KeyError):
                # Skip rows with missing or malformed data
                continue
    return locais


def _distribuir_locais_iniciais(veiculos, locais_ids, locais_dict, max_locais_por_veiculo):
    """
    Distribui locais entre veículos na primeira passada.
    Retorna routes, veiculos_usados e idx.
    """
    routes = {}
    veiculos_usados = []
    idx = 0
    
    for v_idx, veiculo in enumerate(veiculos):
        n_locais = random.randint(1, max_locais_por_veiculo)
        locais_para_veiculo_ids = locais_ids[idx:idx+n_locais]
        if not locais_para_veiculo_ids:
            break
        routes[veiculo] = [locais_dict[lid] for lid in locais_para_veiculo_ids]
        veiculos_usados.append(veiculo)
        idx += n_locais
        if idx >= len(locais_ids):
            break
    
    return routes, veiculos_usados, idx


def _distribuir_locais_restantes(locais_restantes_ids, veiculos_usados, routes, locais_dict, max_locais_por_veiculo):
    """
    Distribui locais restantes entre os veículos já utilizados.
    """
    for i, local_id in enumerate(locais_restantes_ids):
        veiculo_idx = i % len(veiculos_usados)
        veiculo = veiculos_usados[veiculo_idx]
        
        if len(routes[veiculo]) < max_locais_por_veiculo:
            routes[veiculo].append(locais_dict[local_id])
        else:
            # Se o veículo já está cheio, procurar outro veículo disponível
            for v in veiculos_usados:
                if len(routes[v]) < max_locais_por_veiculo:
                    routes[v].append(locais_dict[local_id])
                    break
            else:
                # Se todos os veículos estão cheios, adicionar ao primeiro veículo
                routes[veiculos_usados[0]].append(locais_dict[local_id])


def gerar_genoma_individual(max_locais_por_veiculo=3, veiculos=None, locais=None, local_inicial=None):
    """
    Gera um objeto Genoma com rotas aleatórias.
    - max_locais_por_veiculo: número máximo de locais que um veículo pode visitar
    - veiculos_filepath: caminho opcional para o CSV de veículos
    - locais_filepath: caminho opcional para o CSV de locais
    - local_inicial: objeto Local inicial (opcional)
    """
    if veiculos is None:
        veiculos = load_veiculos_csv()
    if locais is None:
        locais = load_locais_csv()
    locais_ids = [local.id for local in locais]
    random.shuffle(locais_ids)
    # Mapeamento de id para objeto Local
    locais_dict = {local.id: local for local in locais}
    
    # Distribuir locais iniciais
    routes, veiculos_usados, idx = _distribuir_locais_iniciais(
        veiculos, locais_ids, locais_dict, max_locais_por_veiculo
    )
    
    # Garantir que todos os locais sejam incluídos
    if idx < len(locais_ids):
        locais_restantes_ids = locais_ids[idx:]
        _distribuir_locais_restantes(
            locais_restantes_ids, veiculos_usados, routes, locais_dict, max_locais_por_veiculo
        )
    
    if local_inicial is not None:
        return Genoma(routes=routes, local_inicial=local_inicial)
    else:
        return Genoma(routes=routes)

def generate_random_population(population_size: int, veiculos=None, locais=None):    
    if veiculos is None:
        veiculos = load_veiculos_csv()
    if locais is None:
        locais = load_locais_csv()
    return [gerar_genoma_individual(max_locais_por_veiculo=random.randint(1, 6), veiculos=veiculos, locais=locais) for _ in range(population_size)]