## Projeto  
Otimização de logística de entrega.

### Definição do Problema
Durante as eleições, cada cartório eleitoral constitui uma Comissão de Transportes responsável por requisitar e gerenciar veículos cedidos por órgãos estaduais e municipais. Esses veículos são utilizados para:

* Transporte de urnas eletrônicas até os locais de votação;
* Transporte de autoridades eleitorais, servidores e colaboradores.

Cada local de votação pode receber uma ou mais urnas eletrônicas, e cada veículo pode transportar uma ou mais urnas (em caixas). Dessa forma:

* Um único local de votação pode demandar o uso de um ou mais veículos;
* Um único veículo pode atender a múltiplos locais de votação em um mesmo percurso.

Requisito básico:
Toda a demanda de transporte de urnas de todos os locais de votação deve ser integralmente atendida.

### Objetivo
Definir a alocação ideal de veículos e rotas de transporte, de forma a minimizar a quilometragem total percorrida, respeitando a capacidade dos veículos e assegurando o atendimento completo de todos os locais de votação.

### Critérios de Sucesso

A solução para o problema será considerada bem-sucedida se atender simultaneamente aos seguintes critérios:

1. Atendimento Integral da Demanda  
   Todos os locais de votação devem receber a quantidade total de urnas eletrônicas previstas, sem faltas ou excessos.

2. Otimização da Quilometragem Total  
   A soma das distâncias percorridas por todos os veículos deve ser a menor possível, considerando os trajetos entre os pontos de origem e os locais de votação.

3. Respeito à Capacidade dos Veículos  
   Nenhum veículo deve ser sobrecarregado além da sua capacidade máxima de transporte de urnas.


**1) O que está sendo otimizado?**  
Minimizar a distância total percorrida pelos veículos e atender toda demanda dos locais.

**2) Representação da solução (genoma):**
Um cromossomo pode ser representado como **uma lista de rotas**, onde cada rota é uma sequência ordenada de locais atribuídos a um veículo específico.
Exemplo:

```
Genoma = {
  V1: [L5, L7, L2],  # Veículo 1 atende os locais 5, 7 e 2
  V2: [L3, L1],      # Veículo 2 atende os locais 3 e 1
  V3: [L4, L5, L6]   # Veículo 3 atende os locais 4, 5 e 6
}
```

Cada gene representa um local de entrega, e a divisão em sublistas representa a alocação para veículos.

**3) Função de fitness:**


**4) Método de seleção:**

Sugestão: **Torneio binário** ou **Roleta viciada (roulette wheel)**, priorizando soluções com menor fitness (distância + penalidades).


**5) Método de crossover:**

**Crossover baseado em rotas (Route-Based Crossover - RBX)**
Exemplo: seleciona rotas inteiras de um dos pais e preenche o restante com rotas do segundo pai, garantindo que todos os locais sejam atendidos sem duplicação.
Outra alternativa: **Order Crossover (OX)** adaptado à representação.

**6) Método de inicialização:**

* Aleatória respeitando as capacidades dos veículos;
* Heurística simples, como **Nearest Neighbor (vizinho mais próximo)**, para garantir soluções viáveis iniciais e acelerar convergência.


**7) Critério de parada:**

* Número máximo de gerações (ex: 1000);
* Estagnação da fitness (sem melhora após N gerações);
* Valor mínimo de fitness alcançado (limiar ótimo ou aceitável).

## Código

```bash
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
pip install pytest
```
