# Tech Callenge Fase 2

## Definição do desafio
### O PROBLEMA
O desafio consiste em projetar, implementar e testar um sistema que utilize Algoritmos Genéticos para otimizar uma função ou resolver um problema complexo de otimização. Você pode escolher problemas como otimização de rotas, alocação de recursos e design de redes neurais.

### REQUISITOS DO PROJETO
* Definição do Problema: escolha um problema real que possa ser resolvido por meio de otimização genética. Descreva o problema, os
objetivos e os critérios de sucesso.
* Testes e Resultados: realize testes para demonstrar a eficácia do algoritmo. Compare os resultados obtidos com métodos de solução
convencionais.
* Documentação: forneça uma documentação completa do projeto, incluindo descrição do problema, detalhes da implementação do algoritmo, análises de resultados e conclusões.

### ENTREGÁVEL:
* Código-fonte do projeto: deve incluir todos os scripts e códigos utilizados na implementação do algoritmo genético.
* Documento detalhado descrevendo o problema, a abordagem utilizada, os resultados obtidos e as conclusões.
* Um vídeo explicativo do projeto, demonstrando a aplicação prática do algoritmo e discutindo os resultados obtidos.

### Considerações para entrega:
* É preciso mostrar o algoritmo funcionando no vídeo explicativo do projeto.
* O vídeo explicativo deve ter no máximo 10 minutos.
* Os vídeos devem ser enviados para o Youtube, e os códigos devem ser disponibilizados no Github (ou equivalente).
* A entrega deve ser feita em um arquivo PDF, contendo os links do vídeo no YouTube e o repositório do Github com o código nomeado como
“Tech Challenge”.
* Não é preciso apresentar quem são os alunos do grupo no início do vídeo, apenas coloque essa informação na descrição dos vídeos.

### Dicas para uma boa nota:
* Não use o tempo do vídeo explicando como os algoritmos genéticos funcionam, mas sim como as funções específicas que estão utilizando
funcionam.
* Não poderão entregar o projeto utilizando o mesmo tema apresentado em aula.
* Não é preciso relatório em PDF e nem apresentação de slides.
* Foquem em fazer um vídeo de apresentação claro e objetivo.

## Projeto  
Otimização de logística de entrega.

### Definição do Problema
Durante as eleições, cada cartório eleitoral constitui uma Comissão de Transportes responsável por requisitar e gerenciar veículos cedidos por órgãos estaduais e municipais. Esses veículos são utilizados para:

* Transporte de urnas eletrônicas até os locais de votação;
* Transporte de autoridades eleitorais, servidores e colaboradores.

Cada local de votação pode receber uma ou mais urnas eletrônicas, e cada veículo pode transportar uma ou mais urnas (em caixas). Dessa forma:

* Um único local de votação pode demandar o uso de um ou mais veículos;
* Um único veículo pode atender a múltiplos locais de votação em um mesmo percurso.

### Objetivo
Determinar a configuração ideal de alocação de veículos e rotas entre os locais de votação, de forma a minimizar a quilometragem total percorrida.

**1) O que está sendo otimizado?**  
Minimizar a distância total percorrida pelos veículos.

**2) Representação da solução (genoma):**(REVER)     
Um cromossomo pode ser representado como **uma lista de rotas**, onde cada rota é uma sequência ordenada de locais atribuídos a um veículo específico.
Exemplo:

```
Genoma = {
  V1: [L5, L7, L2],  # Veículo 1 atende os locais 5, 7 e 2
  V2: [L3, L1],      # Veículo 2 atende os locais 3 e 1
  V3: [L4, L5, L6]       # Veículo 3 atende os locais 4 e 6
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
* Tempo limite de execução (ex: 1 minuto);
* Valor mínimo de fitness alcançado (limiar ótimo ou aceitável).

## Código

```bash
sudo apt install python3-venv
python3 -m venv env
source env/bin/activate
pip install pytest
```
