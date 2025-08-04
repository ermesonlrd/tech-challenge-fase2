# Comparação Clarke-Wright (Savings Algorithm)

Simulação 1
```bash
=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 203
Número de locais: 17
Local 1040: Demanda 14, Pendente 0 ✓
Local 1104: Demanda 23, Pendente 0 ✓
Local 1112: Demanda 16, Pendente 0 ✓
Local 1120: Demanda 15, Pendente 0 ✓
Local 1147: Demanda 20, Pendente 0 ✓
Local 1180: Demanda 10, Pendente 0 ✓
Local 1210: Demanda 3, Pendente 0 ✓
Local 1279: Demanda 2, Pendente 0 ✓
Local 1341: Demanda 11, Pendente 0 ✓
Local 1368: Demanda 23, Pendente 0 ✓
Local 1384: Demanda 10, Pendente 0 ✓
Local 1392: Demanda 6, Pendente 0 ✓
Local 1406: Demanda 8, Pendente 0 ✓
Local 1430: Demanda 3, Pendente 0 ✓
Local 1457: Demanda 13, Pendente 0 ✓
Local 1465: Demanda 20, Pendente 0 ✓
Local 1511: Demanda 6, Pendente 0 ✓

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 220
Distância Total: 254.51 km
Veículo 0: Capacidade 40, Ociosa 6 ✗, Distância 201.47 km
Veículo 1: Capacidade 60, Ociosa 8 ✗, Distância 7.00 km
Veículo 2: Capacidade 60, Ociosa 3 ✗, Distância 28.46 km
Veículo 3: Capacidade 60, Ociosa 0 ✓, Distância 17.59 km

=== FITNESS ===
Fitness: 424.51

=== ROTAS DO GENOMA ===
V0 MASCA 2021 (40): [L1457 (13), L1511 (6), L1210 (3), L1279 (2), L1180 (10)]
V1 Van16 lugares 2022 (60): [L1040 (14), L1104 (23), L1120 (15)]
V2 Van16 lugares 2023 (60): [L1112 (16), L1147 (20), L1384 (10), L1430 (3), L1406 (8)]
V3 Onibus 2021 (60): [L1392 (6), L1465 (20), L1341 (11), L1368 (23)]

=== STATUS RESUMIDO ===
Demanda Total: 203
Número de locais: 17
Capacidade Total: 220
Distância Total: 254.51 km
Fitness: 424.51



======Clarke-Wright (Savings Algorithm)======

Veículo 1 – Rota: [0, 1120, 1210, 1180, 1279, 1511, 1430, 1392, 1406, 0] – Distância total: 411.49577074717183 km
Veículo 2 – Rota: [0, 1368, 1457, 1384, 1341, 0] – Distância total: 14.450275115036986 km
Veículo 3 – Rota: [0, 1112, 1147, 1104, 0] – Distância total: 10.757015728464008 km
Veículo 0 – Rota: [0, 1465, 1040, 0] – Distância total: 7.650888864298576 km
```

Simulação 2
```bash
=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 203
Número de locais: 17
Local 1040: Demanda 14, Pendente 0 ✓
Local 1104: Demanda 23, Pendente 0 ✓
Local 1112: Demanda 16, Pendente 0 ✓
Local 1120: Demanda 15, Pendente 0 ✓
Local 1147: Demanda 20, Pendente 0 ✓
Local 1180: Demanda 10, Pendente 0 ✓
Local 1210: Demanda 3, Pendente 0 ✓
Local 1279: Demanda 2, Pendente 0 ✓
Local 1341: Demanda 11, Pendente 0 ✓
Local 1368: Demanda 23, Pendente 0 ✓
Local 1384: Demanda 10, Pendente 0 ✓
Local 1392: Demanda 6, Pendente 0 ✓
Local 1406: Demanda 8, Pendente 0 ✓
Local 1430: Demanda 3, Pendente 0 ✓
Local 1457: Demanda 13, Pendente 0 ✓
Local 1465: Demanda 20, Pendente 0 ✓
Local 1511: Demanda 6, Pendente 0 ✓

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 220
Distância Total: 285.34 km
Veículo 0: Capacidade 40, Ociosa 0 ✓, Distância 34.72 km
Veículo 1: Capacidade 60, Ociosa 0 ✓, Distância 24.98 km
Veículo 2: Capacidade 60, Ociosa 8 ✗, Distância 210.79 km
Veículo 3: Capacidade 60, Ociosa 9 ✗, Distância 14.86 km

=== FITNESS ===
Fitness: 455.34

=== ROTAS DO GENOMA ===
V0 MASCA 2021 (40): [L1457 (13), L1430 (3), L1104 (23), L1341 (11)]
V1 Van16 lugares 2022 (60): [L1040 (14), L1120 (15), L1465 (20), L1511 (6), L1147 (20)]
V2 Van16 lugares 2023 (60): [L1457 (13), L1465 (20), L1368 (23), L1392 (6), L1406 (8), L1210 (3), L1279 (2), L1180 (10)]
V3 Onibus 2021 (60): [L1112 (16), L1147 (20), L1341 (11), L1384 (10), L1406 (8)]

=== STATUS RESUMIDO ===
Demanda Total: 203
Número de locais: 17
Capacidade Total: 220
Distância Total: 285.34 km
Fitness: 455.34



======Clarke-Wright (Savings Algorithm)======

Veículo 1 – Rota: [0, 1120, 1210, 1180, 1279, 1511, 1430, 1392, 1406, 0] – Distância total: 411.49577074717183 km
Veículo 2 – Rota: [0, 1368, 1457, 1384, 1341, 0] – Distância total: 14.450275115036986 km
Veículo 3 – Rota: [0, 1112, 1147, 1104, 0] – Distância total: 10.757015728464008 km
Veículo 0 – Rota: [0, 1465, 1040, 0] – Distância total: 7.650888864298576 km
```

Simulação 3
```bash
=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 203
Número de locais: 17
Local 1040: Demanda 14, Pendente 0 ✓
Local 1104: Demanda 23, Pendente 0 ✓
Local 1112: Demanda 16, Pendente 0 ✓
Local 1120: Demanda 15, Pendente 0 ✓
Local 1147: Demanda 20, Pendente 0 ✓
Local 1180: Demanda 10, Pendente 0 ✓
Local 1210: Demanda 3, Pendente 0 ✓
Local 1279: Demanda 2, Pendente 0 ✓
Local 1341: Demanda 11, Pendente 0 ✓
Local 1368: Demanda 23, Pendente 0 ✓
Local 1384: Demanda 10, Pendente 0 ✓
Local 1392: Demanda 6, Pendente 0 ✓
Local 1406: Demanda 8, Pendente 0 ✓
Local 1430: Demanda 3, Pendente 0 ✓
Local 1457: Demanda 13, Pendente 0 ✓
Local 1465: Demanda 20, Pendente 0 ✓
Local 1511: Demanda 6, Pendente 0 ✓

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 220
Distância Total: 268.25 km
Veículo 0: Capacidade 40, Ociosa 5 ✗, Distância 18.65 km
Veículo 1: Capacidade 60, Ociosa 2 ✗, Distância 200.70 km
Veículo 2: Capacidade 60, Ociosa 1 ✗, Distância 20.68 km
Veículo 3: Capacidade 60, Ociosa 9 ✗, Distância 28.21 km

=== FITNESS ===
Fitness: 438.25

=== ROTAS DO GENOMA ===
V0 MASCA 2021 (40): [L1040 (14), L1406 (8), L1384 (10), L1430 (3)]
V1 Van16 lugares 2022 (60): [L1104 (23), L1465 (20), L1210 (3), L1279 (2), L1180 (10)]
V2 Van16 lugares 2023 (60): [L1120 (15), L1457 (13), L1341 (11), L1040 (14), L1147 (20)]
V3 Onibus 2021 (60): [L1147 (20), L1511 (6), L1112 (16), L1341 (11), L1392 (6), L1368 (23)]

=== STATUS RESUMIDO ===
Demanda Total: 203
Número de locais: 17
Capacidade Total: 220
Distância Total: 268.25 km
Fitness: 438.25



======Clarke-Wright (Savings Algorithm)======

Veículo 1 – Rota: [0, 1120, 1210, 1180, 1279, 1511, 1430, 1392, 1406, 0] – Distância total: 411.49577074717183 km
Veículo 2 – Rota: [0, 1368, 1457, 1384, 1341, 0] – Distância total: 14.450275115036986 km
Veículo 3 – Rota: [0, 1112, 1147, 1104, 0] – Distância total: 10.757015728464008 km
Veículo 0 – Rota: [0, 1465, 1040, 0] – Distância total: 7.650888864298576 km
```

Simulação 4
```bash
=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 203
Número de locais: 17
Local 1040: Demanda 14, Pendente 0 ✓
Local 1104: Demanda 23, Pendente 0 ✓
Local 1112: Demanda 16, Pendente 0 ✓
Local 1120: Demanda 15, Pendente 0 ✓
Local 1147: Demanda 20, Pendente 0 ✓
Local 1180: Demanda 10, Pendente 0 ✓
Local 1210: Demanda 3, Pendente 0 ✓
Local 1279: Demanda 2, Pendente 0 ✓
Local 1341: Demanda 11, Pendente 0 ✓
Local 1368: Demanda 23, Pendente 0 ✓
Local 1384: Demanda 10, Pendente 0 ✓
Local 1392: Demanda 6, Pendente 0 ✓
Local 1406: Demanda 8, Pendente 0 ✓
Local 1430: Demanda 3, Pendente 0 ✓
Local 1457: Demanda 13, Pendente 0 ✓
Local 1465: Demanda 20, Pendente 0 ✓
Local 1511: Demanda 6, Pendente 0 ✓

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 220
Distância Total: 268.21 km
Veículo 0: Capacidade 40, Ociosa 2 ✗, Distância 196.54 km
Veículo 1: Capacidade 60, Ociosa 1 ✗, Distância 33.16 km
Veículo 2: Capacidade 60, Ociosa 10 ✗, Distância 16.18 km
Veículo 3: Capacidade 60, Ociosa 4 ✗, Distância 22.33 km

=== FITNESS ===
Fitness: 438.21

=== ROTAS DO GENOMA ===
V0 MASCA 2021 (40): [L1104 (23), L1210 (3), L1279 (2), L1180 (10)]
V1 Van16 lugares 2022 (60): [L1120 (15), L1430 (3), L1406 (8), L1457 (13), L1465 (20)]
V2 Van16 lugares 2023 (60): [L1457 (13), L1384 (10), L1341 (11), L1392 (6), L1368 (23)]
V3 Onibus 2021 (60): [L1040 (14), L1147 (20), L1112 (16), L1511 (6), L1392 (6)]

=== STATUS RESUMIDO ===
Demanda Total: 203
Número de locais: 17
Capacidade Total: 220
Distância Total: 268.21 km
Fitness: 438.21



======Clarke-Wright (Savings Algorithm)======

Veículo 1 – Rota: [0, 1120, 1210, 1180, 1279, 1511, 1430, 1392, 1406, 0] – Distância total: 411.49577074717183 km
Veículo 2 – Rota: [0, 1368, 1457, 1384, 1341, 0] – Distância total: 14.450275115036986 km
Veículo 3 – Rota: [0, 1112, 1147, 1104, 0] – Distância total: 10.757015728464008 km
Veículo 0 – Rota: [0, 1465, 1040, 0] – Distância total: 7.650888864298576 km
```

Simulação 5
```bash
=== STATUS DAS DEMANDAS DOS LOCAIS ===
Demanda Total: 203
Número de locais: 17
Local 1040: Demanda 14, Pendente 0 ✓
Local 1104: Demanda 23, Pendente 0 ✓
Local 1112: Demanda 16, Pendente 0 ✓
Local 1120: Demanda 15, Pendente 0 ✓
Local 1147: Demanda 20, Pendente 0 ✓
Local 1180: Demanda 10, Pendente 0 ✓
Local 1210: Demanda 3, Pendente 0 ✓
Local 1279: Demanda 2, Pendente 0 ✓
Local 1341: Demanda 11, Pendente 0 ✓
Local 1368: Demanda 23, Pendente 0 ✓
Local 1384: Demanda 10, Pendente 0 ✓
Local 1392: Demanda 6, Pendente 0 ✓
Local 1406: Demanda 8, Pendente 0 ✓
Local 1430: Demanda 3, Pendente 0 ✓
Local 1457: Demanda 13, Pendente 0 ✓
Local 1465: Demanda 20, Pendente 0 ✓
Local 1511: Demanda 6, Pendente 0 ✓

=== STATUS DAS CAPACIDADES E DISTÂNCIAS DOS VEÍCULOS ===
Capacidade Total: 220
Distância Total: 267.26 km
Veículo 0: Capacidade 40, Ociosa 0 ✓, Distância 7.56 km
Veículo 1: Capacidade 60, Ociosa 6 ✗, Distância 19.10 km
Veículo 2: Capacidade 60, Ociosa 11 ✗, Distância 205.88 km
Veículo 3: Capacidade 60, Ociosa 0 ✓, Distância 34.72 km

=== FITNESS ===
Fitness: 437.26

=== ROTAS DO GENOMA ===
V0 MASCA 2021 (40): [L1112 (16), L1147 (20), L1040 (14)]
V1 Van16 lugares 2022 (60): [L1120 (15), L1040 (14), L1392 (6), L1384 (10), L1457 (13)]
V2 Van16 lugares 2023 (60): [L1406 (8), L1465 (20), L1511 (6), L1210 (3), L1279 (2), L1180 (10)]
V3 Onibus 2021 (60): [L1368 (23), L1430 (3), L1104 (23), L1341 (11)]

=== STATUS RESUMIDO ===
Demanda Total: 203
Número de locais: 17
Capacidade Total: 220
Distância Total: 267.26 km
Fitness: 437.26



======Clarke-Wright (Savings Algorithm)======

Veículo 1 – Rota: [0, 1120, 1210, 1180, 1279, 1511, 1430, 1392, 1406, 0] – Distância total: 411.49577074717183 km
Veículo 2 – Rota: [0, 1368, 1457, 1384, 1341, 0] – Distância total: 14.450275115036986 km
Veículo 3 – Rota: [0, 1112, 1147, 1104, 0] – Distância total: 10.757015728464008 km
Veículo 0 – Rota: [0, 1465, 1040, 0] – Distância total: 7.650888864298576 km
```