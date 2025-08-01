# Tech Callenge Fase 2
Projeto de solução ao [desafio proposto](DESAFIO.md).

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

## Detalhes da implementação do algoritmo
### Principais características

* População: conjunto de soluções (indivíduos) avaliadas em cada geração.

* Cromossomo/Genoma: representação da solução, com estrutura específica.

* Função de fitness: avalia a qualidade de cada indivíduo.

* Seleção: escolhe os melhores indivíduos para reprodução (ex.: roleta, torneio).

* Crossover: combina dois indivíduos para gerar novos (filhos) com características de ambos.

* Mutação: altera aleatoriamente partes do indivíduo para manter diversidade.

* Elitismo (opcional): garante que os melhores indivíduos sejam preservados.

* Critério de parada: define quando o algoritmo encerra (ex.: número de gerações ou estagnação do fitness).

### Arquivos

- **veiculo.py**: Representação do veículo com sua capacidade.
- **local.py**: Representação do local com sua demanda. Utiliza coordenadas geográficas.
- **population.py**: Inclui funções que carregam os veiculos e locais a partir dos arquivos .CSV. Funções para gerar um genoma individual e uma população de genomas.
- **genoma.py**: A representação do genoma com funções de fitness, crossover e mutação.
- **main.py**: Inicia a população, aplica seleção, elitismo e o critério de parada.

### Ambiente e dependências

```bash
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### Representação do genoma
O genoma é representado como **uma lista de rotas**, onde cada rota é uma sequência ordenada de locais atribuídos a um veículo específico. Ele também possui um local inicial de partida das rotas, por padrão o Fórum Eleitoral de Porto Velho/RO.

Considerando uma rota como a representada no formato:
```bash 
Veiculo{id} {modelo} {ano} ({capacidade}): [Local{numero_local} ({demanda}), Local{numero_local} ({demanda})]
```

Segue um exemplo de estrutura básica de um genoma:
```bash
Genoma = {
   local_inicial: L0,
   rotas: {
      V0 HILUX 2020 (15): [L1457 (4), L1635 (5)]
      V1 L200 2011 (8): [L1830 (8), L1449 (13)]
      V2 ETIOS 2020 (4): [L1740 (4), L1775 (10)]
      V3 ETIOS 2015 (4): [L1392 (12), L1597 (12)]
      V4 L200 2014 (16): [L1732 (4), L1716 (9)]
      V5 Onibus 2020 (40): [L1686 (22), L1694 (4)]
      V6 VAN (24 LUGARES) 2022 (40): [L1660 (2), L1147 (8)]
      V7 MASCA 2021 (40): [L1082 (17), L1562 (10)]
      V8 ETIOS 2015 (4): [L1414 (12), L1643 (3)]
      V9 SW4 2015 (5): [L1546 (8)]
   }
}
```
#### Inicialização
Os locais e os veiculos foram selecionados de exemplos reais de Eleições anteriores. Eles estão localizados nos arquivos [data/locais-votacao.csv](data/locais-votacao.csv) e [data/veiculos.csv](data/veiculos.csv).

A função **gerar_genoma_individual** definida no arquivo **population.py** cria e retorna um objeto Genoma com rotas aleatórias, distribuindo locais entre veículos de forma controlada.

Funcionamento resumido:

1. Parâmetro de controle: max_locais_por_veiculo define o número máximo de locais que cada veículo pode visitar. Ele limita a quantidade de locais atribuídos a cada veículo durante a distribuição.

2. Carregamento de dados: Se os parâmetros veiculos e locais não forem informados, os dados são carregados de arquivos CSV.

3. Embaralhamento dos locais: A lista de IDs dos locais é embaralhada aleatoriamente para garantir diversidade nas soluções.

4. Distribuição inicial: A função _distribuir_locais_iniciais distribui um número aleatório de locais (entre 1 e max_locais_por_veiculo) entre os veículos disponíveis até que todos os locais sejam alocados ou os veículos se esgotem.

5. Distribuição dos locais restantes: Se restarem locais, a função _distribuir_locais_restantes os aloca entre os veículos já usados, respeitando o limite de max_locais_por_veiculo por veículo.

6. Criação do genoma: O objeto Genoma é criado com as rotas geradas, e com local_inicial, se fornecido.

A classe **Genoma** representa uma solução composta por rotas atribuídas a veículos, com métricas associadas ao atendimento da demanda e ao uso da capacidade.

Funcionamento da inicialização (__init__):
1. Parâmetros de entrada:

   routes: dicionário com veículos e suas respectivas rotas (lista de locais).

   local_inicial: ponto de partida das rotas (default: Fórum Eleitoral de Porto Velho/RO).

   fitness: valor inicial da função objetivo (default: 0.0).

2. Armazenamento dos dados:

   As rotas são atribuídas ao atributo self.routes.

   O local_inicial é definido; caso não seja informado, utiliza um ponto padrão pré-configurado.

3. Inicialização de métricas (_inicializar_metricas):

   Calcula:

   Demanda pendente por local e total.

   Capacidade ociosa por veículo e total.

   Distância percorrida por veículo (inicialmente 0).

   Agrupa essas informações em uma instância de MetricasGenoma.

4. Processamento das rotas (_processar_rotas):

   Para cada veículo:

     Calcula a distância de Manhattan total percorrida (considerando o ponto de partida e cada par de locais consecutivos). Utiliza a função auxilizar **calcular_distancia_manhattan** do arquivo **distancia_geografica.py**.

     Atualiza as métricas de atendimento de demanda conforme a capacidade do veículo.

   Ao final, consolida as métricas globais:

     Soma total das distâncias.

     Soma da demanda não atendida.

     Soma da capacidade não utilizada.

Visualizando um exemplo:
```bash
source env/bin/activate
python test_genoma_individual.py

=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 167
Número de locais: 19
Local 1082: Demanda 17, Pendente 9 ✗
Local 1147: Demanda 8, Pendente 4 ✗
Local 1392: Demanda 12, Pendente 12 ✗
Local 1414: Demanda 12, Pendente 8 ✗
Local 1449: Demanda 13, Pendente 0 ✓
Local 1457: Demanda 4, Pendente 4 ✗
Local 1546: Demanda 8, Pendente 8 ✗
Local 1562: Demanda 10, Pendente 0 ✓
Local 1597: Demanda 12, Pendente 0 ✓
Local 1635: Demanda 5, Pendente 0 ✓
Local 1643: Demanda 3, Pendente 0 ✓
Local 1660: Demanda 2, Pendente 2 ✗
Local 1686: Demanda 22, Pendente 0 ✓
Local 1694: Demanda 4, Pendente 0 ✓
Local 1716: Demanda 9, Pendente 0 ✓
Local 1732: Demanda 4, Pendente 2 ✗
Local 1740: Demanda 4, Pendente 4 ✗
Local 1775: Demanda 10, Pendente 0 ✓
Local 1830: Demanda 8, Pendente 8 ✗

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 176
Distância Total: 2906.78 km
Veículo 0: Capacidade 15, Ociosa 3 ✗, Distância 407.59 km
Veículo 1: Capacidade 8, Ociosa 0 ✓, Distância 16.00 km
Veículo 2: Capacidade 4, Ociosa 0 ✓, Distância 69.13 km
Veículo 3: Capacidade 4, Ociosa 0 ✓, Distância 205.75 km
Veículo 4: Capacidade 16, Ociosa 6 ✗, Distância 299.49 km
Veículo 5: Capacidade 40, Ociosa 27 ✗, Distância 7.18 km
Veículo 6: Capacidade 40, Ociosa 31 ✗, Distância 380.96 km
Veículo 7: Capacidade 40, Ociosa 3 ✗, Distância 761.01 km
Veículo 8: Capacidade 4, Ociosa 0 ✓, Distância 109.94 km
Veículo 9: Capacidade 5, Ociosa 0 ✓, Distância 649.73 km

=== FITNESS ===
Fitness: 15806.78

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1597 (12)]
V1 L200 2011 (8): [L1082 (17), L1392 (12), L1457 (4)]
V2 ETIOS 2020 (4): [L1414 (12), L1830 (8), L1660 (2)]
V3 ETIOS 2015 (4): [L1694 (4)]
V4 L200 2014 (16): [L1562 (10)]
V5 Onibus 2020 (40): [L1449 (13)]
V6 VAN (24 LUGARES) 2022 (40): [L1716 (9)]
V7 MASCA 2021 (40): [L1775 (10), L1635 (5), L1686 (22)]
V8 ETIOS 2015 (4): [L1147 (8), L1546 (8)]
V9 SW4 2015 (5): [L1643 (3), L1732 (4), L1740 (4)]
```

#### Função de fitness
Avalia a qualidade de cada indivíduo.

Fórmula:
```python
# Constantes para cálculo de fitness
PENALIDADE_DEMANDA = 200.0
PENALIDADE_CAPACIDADE = 10.0

fitness = 
    distância_total_percorrida +
    (demanda_pendente_total × PENALIDADE_DEMANDA) +
    (capacidade_ociosa_total × PENALIDADE_CAPACIDADE)
```

O método calcular_fitness calcula o custo da solução representada pelo genoma com base em três critérios:

1. Distância percorrida total (distancia_percorrida_total)

   Contribui diretamente para o valor do fitness.

   Peso implícito: 1.

2. Demanda não atendida (demanda_pendente_total)

   Penaliza fortemente soluções que deixam demanda sem atendimento.

   Peso (penalidade): 200.0 → impacto mais severo no fitness.

3. Capacidade não utilizada (capacidade_ociosa_total)

   Penaliza a ociosidade dos veículos.

   Peso (penalidade): 10.0 → penalização moderada.

O fator com maior impacto é a demanda não atendida, garantindo prioridade ao atendimento integral das necessidades logísticas. 

Quanto menor o fitness, melhor a eficiência da solução.

#### Função Crossover
A função crossover combina dois genomas (self e parceiro) para gerar um novo genoma filho com características de ambos. A função crossover posui as seguintes etapas:

**1. Mapeamento de locais únicos**

* Todos os locais dos dois genomas são indexados por ID, garantindo unicidade.

* Em caso de conflito (mesmo ID), o local de self tem prioridade.

**2. Identificação dos veículos**

   Veículos são classificados em:

* Exclusivos de self

* Exclusivos do parceiro

* Compartilhados (presentes em ambos)

**3. Tratamento dos veículos exclusivos**

* Rotas dos veículos exclusivos são copiadas diretamente para o filho, respeitando a unicidade dos locais.

**4. Combinação dos veículos compartilhados**

   Para cada veículo compartilhado:

* As rotas de ambos os genomas são unidas por ID, eliminando repetições.

* A lista resultante é convertida em objetos a partir do dicionário locais_unicos.

* O tamanho final da rota do filho é escolhido aleatoriamente entre:

  * Tamanho da rota de self

  * Tamanho da rota do parceiro

  * Média dos dois tamanhos

  * Soma dos dois tamanhos

* O número de locais escolhidos é limitado à quantidade de locais únicos combinados.

* Os locais são selecionados aleatoriamente e atribuídos ao veículo correspondente no filho.

**5. Distribuição de locais restantes**

Locais ainda não atribuídos são distribuídos aleatoriamente entre os veículos já presentes no filho.


Resultado

O genoma filho contém:

  * Todos os locais únicos (sem duplicidade)

  * Referências consistentes aos objetos de local

  * Estrutura de rotas por veículo respeitando os vínculos originais

Essa abordagem assegura diversidade genética e evita perda de informação.

Visualizando um exemplo:
```bash
source env/bin/activate
python test_crossover.py

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1597 (12), L1414 (12), L1740 (4)]
V1 L200 2011 (8): [L1643 (3)]
V2 ETIOS 2020 (4): [L1147 (8)]
V3 ETIOS 2015 (4): [L1082 (17), L1660 (2), L1686 (22)]
V4 L200 2014 (16): [L1392 (12), L1732 (4), L1635 (5)]
V5 Onibus 2020 (40): [L1716 (9), L1775 (10)]
V6 VAN (24 LUGARES) 2022 (40): [L1457 (4), L1449 (13), L1694 (4)]
V7 MASCA 2021 (40): [L1562 (10), L1830 (8), L1546 (8)]

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1597 (12)]
V1 L200 2011 (8): [L1694 (4), L1449 (13), L1635 (5)]
V2 ETIOS 2020 (4): [L1562 (10)]
V3 ETIOS 2015 (4): [L1716 (9), L1740 (4), L1147 (8)]
V4 L200 2014 (16): [L1775 (10), L1414 (12)]
V5 Onibus 2020 (40): [L1392 (12), L1082 (17)]
V6 VAN (24 LUGARES) 2022 (40): [L1546 (8)]
V7 MASCA 2021 (40): [L1732 (4)]
V8 ETIOS 2015 (4): [L1830 (8)]
V9 SW4 2015 (5): [L1643 (3), L1686 (22), L1660 (2)]
V10 S10 2021 (15): [L1457 (4)]

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1414 (12), L1597 (12), L1740 (4)]
V1 L200 2011 (8): [L1643 (3), L1449 (13), L1694 (4), L1635 (5)]
V2 ETIOS 2020 (4): [L1562 (10), L1147 (8)]
V3 ETIOS 2015 (4): [L1686 (22), L1660 (2), L1740 (4)]
V4 L200 2014 (16): [L1414 (12), L1732 (4), L1392 (12), L1775 (10), L1635 (5)]
V5 Onibus 2020 (40): [L1716 (9), L1392 (12)]
V6 VAN (24 LUGARES) 2022 (40): [L1457 (4), L1546 (8), L1449 (13)]
V7 MASCA 2021 (40): [L1732 (4), L1562 (10), L1830 (8), L1546 (8)]
V8 ETIOS 2015 (4): [L1830 (8)]
V9 SW4 2015 (5): [L1643 (3), L1686 (22), L1660 (2), L1082 (17)]
V10 S10 2021 (15): [L1457 (4)]

=== STATUS RESUMIDO ===
Demanda Total: 167
Número de locais: 19
Capacidade Total: 191
Distância Total: 5463.59 km
Fitness: 21453.59
```

#### Função mutate

A função mutate aplica mutação nas rotas do genoma, com três tipos de alteração possíveis, controladas pela taxa de mutação:

_mutar_trocar_posicoes: troca a posição de dois locais dentro da mesma rota, se houver pelo menos dois locais e a taxa permitir.

_mutar_mover_entre_veiculos: move um local aleatório de uma rota para outra, evitando locais duplicados na mesma rota.

_mutar_remover_excedentes: remove locais de rotas que excedem a capacidade do veículo e redistribui os locais removidos entre outros veículos.

Se alguma mutação for aplicada, as métricas são recalculadas. A função retorna True caso qualquer mutação ocorra.

Visualizando um exemplo:

```bash
python test_mutate.py 

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1635 (5)]
V1 L200 2011 (8): [L1546 (8), L1414 (12), L1597 (12)]
V2 ETIOS 2020 (4): [L1716 (9)]
V3 ETIOS 2015 (4): [L1732 (4), L1449 (13)]
V4 L200 2014 (16): [L1775 (10), L1082 (17)]
V5 Onibus 2020 (40): [L1740 (4), L1457 (4), L1392 (12)]
V6 VAN (24 LUGARES) 2022 (40): [L1686 (22), L1660 (2), L1562 (10)]
V7 MASCA 2021 (40): [L1830 (8)]
V8 ETIOS 2015 (4): [L1694 (4), L1147 (8)]
V9 SW4 2015 (5): [L1643 (3)]

=== STATUS RESUMIDO ===
Demanda Total: 167
Número de locais: 19
Capacidade Total: 176
Distância Total: 3009.75 km
Fitness: 15909.75

=== ROTAS DO GENOMA ===
V0 HILUX 2020 (15): [L1635 (5)]
V1 L200 2011 (8): [L1546 (8), L1414 (12), L1597 (12)]
V2 ETIOS 2020 (4): [L1716 (9)]
V3 ETIOS 2015 (4): [L1449 (13), L1732 (4)]
V4 L200 2014 (16): [L1082 (17), L1775 (10)]
V5 Onibus 2020 (40): [L1457 (4), L1740 (4), L1392 (12)]
V6 VAN (24 LUGARES) 2022 (40): [L1686 (22), L1562 (10), L1660 (2)]
V7 MASCA 2021 (40): [L1643 (3), L1830 (8)]
V8 ETIOS 2015 (4): [L1694 (4), L1147 (8)]
V9 SW4 2015 (5): []

=== STATUS RESUMIDO ===
Demanda Total: 167
Número de locais: 19
Capacidade Total: 176
Distância Total: 3129.84 km
Fitness: 16029.84
```

### Algoritmo genético
No arquivo main.py está o código do algoritmo genético, com os seguintes passos:

1. Inicialização

   * Carrega dados de veículos e locais.

   * Gera uma população inicial aleatória com 500 genomas.

2. Loop Evolutivo (10.000 gerações)

   Para cada geração:

   a. Avaliação (Seleção natural)

      * Calcula o fitness de cada indivíduo.

      * Ordena a população e seleciona os 10 melhores (elitismo).

      * Armazena o melhor fitness e solução da geração.

   b. Nova População

      * Mantém os elites.

      * Adiciona 20 novos indivíduos aleatórios.

      Cruzamentos:

      * Cruza os novos aleatórios com elites → aplica mutação.

      * Completa a população com cruzamentos aleatórios (usando roleta viciada para seleção dos pais com base no fitness) → aplica mutação.

3. Finalização

    * Imprime o melhor fitness obtido.

    * Exibe a solução final (status e rotas).



## **Compare os resultados obtidos com métodos de solução convencionais**
O algoritmo de Clarke-Wright, também conhecido como Savings Algorithm, é uma heurística clássica para resolver o Problema de Roteamento de Veículos (VRP). Ele é eficiente e relativamente simples de implementar, sendo uma boa referência para comparação.

### Clarke-Wright (Savings Algorithm)
O Algorimo "Savings Algorithm" possui uma definição de problema um pouco diferente da apresentada.

"O número máximo de veículos é n, que seria a situação em que exatamente um veículo é designado para cada local de entrega. Cada veículo tem uma capacidade máxima de carga G, e cada veículo tem uma distância máxima D que pode percorrer. Por fim, cada local de entrega vi (para i ≥ 1) tem um valor de demanda wi.

O problema de roteamento de veículos consiste em encontrar rotas de menor custo de forma que:

1) Cada local de entrega seja visitado exatamente uma vez por apenas um veículo;

2) Todos os veículos comecem e terminem no depósito;

3) As restrições laterais de capacidade máxima do veículo e distância de viagem sejam atendidas.
"

Diferenças para o problema apresentado no projeto:

1) Um local pode ser visitado por mais de um veículo. A maioria dos veículos disponíveis não atende os locais em sua totalidade.

2) A rota de cada veículo finaliza no último local. O trajeto de retorno é irrelavante para o problema apresentado.

3) Sem restrições de distância.

No algoritmo de Clarke-Wright, a abordagem parte de uma solução inicial trivial:

Um veículo para cada local de votação (cliente), indo do depósito (cartório) ao local e retornando.

A seguir, o algoritmo tenta combinar pares de rotas (clientes) com o objetivo de economizar distância, desde que:

1) A capacidade do veículo não seja excedida.

2) As rotas combinadas formem uma rota viável.

Optou-se por ajustar o conjuntos de veículos e locais para uma comparação aproximada.

Fonte: https://aswani.ieor.berkeley.edu/teaching/FA15/151/lecture_notes/ieor151_lec18.pdf


Mais informações em [Peguntas e respotas sobre o projeto](PERGUNTAS.md).