# Reporte v2_mix4h_hash (desempate: hash)

Estados decidibles analizados: 2301 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.279 | 0.226 | 0.282 (n=1173) | 0.300 (n=626) | 0.280 (n=339) | 0.172 (n=163) | 0.279 |
| sin_D2 | 0.269 | 0.221 | 0.272 (n=1173) | 0.299 (n=626) | 0.245 (n=339) | 0.178 (n=163) | 0.269 |
| sin_H | 0.361 | 0.291 | 0.447 (n=1173) | 0.299 (n=626) | 0.257 (n=339) | 0.196 (n=163) | 0.361 |
| sin_V | 0.195 | 0.164 | 0.203 (n=1173) | 0.232 (n=626) | 0.165 (n=339) | 0.061 (n=163) | 0.195 |
| sin_D1D2 | 0.340 | 0.278 | 0.352 (n=1173) | 0.350 (n=626) | 0.342 (n=339) | 0.215 (n=163) | 0.340 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.093 | 0.093 | 0.075 | 0.251 (n=215) |
| sin_D1 / sin_H | 0.104 | 0.123 | 0.101 | 0.261 (n=283) |
| sin_D1 / sin_V | 0.056 | 0.064 | 0.054 | 0.304 (n=148) |
| sin_D1 / sin_D1D2 | 0.298 | 0.158 | 0.095 | 0.280 (n=364) |
| sin_D2 / sin_H | 0.123 | 0.123 | 0.097 | 0.230 (n=283) |
| sin_D2 / sin_V | 0.048 | 0.061 | 0.052 | 0.229 (n=140) |
| sin_D2 / sin_D1D2 | 0.308 | 0.156 | 0.091 | 0.276 (n=359) |
| sin_H / sin_V | -0.036 | 0.063 | 0.070 | 0.178 (n=146) |
| sin_H / sin_D1D2 | 0.116 | 0.149 | 0.123 | 0.216 (n=343) |
| sin_V / sin_D1D2 | -0.009 | 0.065 | 0.066 | 0.215 (n=149) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.726 | 0.726 | 0.731 | -0.005 | 0.093 (n=215) | 0.107/0.105/0.059/0.018 |
| sin_D1 + sin_H | 0.680 | 0.680 | 0.721 | -0.041 | 0.123 (n=283) | 0.165/0.102/0.065/0.025 |
| sin_D1 + sin_V | 0.763 | 0.763 | 0.805 | -0.042 | 0.064 (n=148) | 0.073/0.073/0.041/0.012 |
| sin_D1 + sin_D1D2 | 0.690 | 0.690 | 0.721 | -0.031 | 0.158 (n=364) | 0.170/0.161/0.150/0.080 |
| sin_D2 + sin_H | 0.685 | 0.685 | 0.731 | -0.046 | 0.123 (n=283) | 0.155/0.112/0.071/0.043 |
| sin_D2 + sin_V | 0.768 | 0.768 | 0.805 | -0.037 | 0.061 (n=140) | 0.071/0.058/0.056/0.012 |
| sin_D2 + sin_D1D2 | 0.696 | 0.696 | 0.731 | -0.036 | 0.156 (n=359) | 0.155/0.187/0.142/0.074 |
| sin_H + sin_V | 0.722 | 0.722 | 0.805 | -0.083 | 0.063 (n=146) | 0.084/0.065/0.021/0.000 |
| sin_H + sin_D1D2 | 0.650 | 0.650 | 0.660 | -0.010 | 0.149 (n=343) | 0.202/0.125/0.074/0.018 |
| sin_V + sin_D1D2 | 0.732 | 0.732 | 0.805 | -0.073 | 0.065 (n=149) | 0.072/0.069/0.059/0.012 |
| sin_D1 + sin_D2 + sin_H | 0.697 | 0.761 | 0.731 | +0.029 | 0.051 (n=117) | 0.073/0.043/0.012/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.752 | 0.830 | 0.805 | +0.025 | 0.027 (n=63) | 0.040/0.021/0.009/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.704 | 0.744 | 0.731 | +0.013 | 0.071 (n=163) | 0.086/0.075/0.035/0.018 |
| sin_D1 + sin_H + sin_V | 0.722 | 0.807 | 0.805 | +0.002 | 0.032 (n=73) | 0.044/0.030/0.006/0.000 |
| sin_D1 + sin_H + sin_D1D2 | 0.673 | 0.733 | 0.721 | +0.012 | 0.077 (n=178) | 0.108/0.061/0.035/0.006 |
| sin_D1 + sin_V + sin_D1D2 | 0.729 | 0.791 | 0.805 | -0.014 | 0.038 (n=88) | 0.049/0.035/0.024/0.000 |
| sin_D2 + sin_H + sin_V | 0.725 | 0.805 | 0.805 | +0.000 | 0.030 (n=69) | 0.041/0.029/0.009/0.000 |
| sin_D2 + sin_H + sin_D1D2 | 0.677 | 0.732 | 0.731 | +0.001 | 0.079 (n=181) | 0.101/0.073/0.041/0.012 |
| sin_D2 + sin_V + sin_D1D2 | 0.732 | 0.798 | 0.805 | -0.007 | 0.039 (n=90) | 0.045/0.040/0.029/0.012 |
| sin_H + sin_V + sin_D1D2 | 0.701 | 0.790 | 0.805 | -0.015 | 0.035 (n=81) | 0.049/0.032/0.012/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.724 | 0.857 | 0.805 | +0.052 | 0.018 (n=41) | 0.028/0.011/0.003/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.688 | 0.785 | 0.731 | +0.054 | 0.041 (n=94) | 0.062/0.029/0.009/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.729 | 0.833 | 0.805 | +0.028 | 0.022 (n=50) | 0.034/0.014/0.003/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.706 | 0.833 | 0.805 | +0.028 | 0.025 (n=58) | 0.038/0.019/0.006/0.000 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.709 | 0.830 | 0.805 | +0.025 | 0.023 (n=52) | 0.032/0.018/0.009/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.711 | 0.861 | 0.805 | +0.056 | 0.016 (n=36) | 0.026/0.008/0.003/0.000 |

## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado

Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.

| conjunto | entropía media | estados con mezcla unánime |
|---|---|---|
| sin_D1 + sin_D2 | 0.260 | 0.312 |
| sin_D1 + sin_D2 + sin_H | 0.399 | 0.121 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.472 | 0.053 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.523 | 0.031 |

## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n=215 de 2301)

```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . .
. . O O . X .
. . X X O O X
1 2 3 4 5 6 7
jugadas: 35764463  (mueve jugador 1, ply 8)
óptimas reales: [4]   sin_D1 juega [2]   sin_D2 juega [3]   resultados por columna: {'1': -1, '2': -1, '3': 0, '4': 1, '5': -1, '6': 0, '7': -1}
```
```
. . . . . . .
. . . . . . .
. . . X . . .
O . . O . . .
X . O X . . O
O . X X O X X
1 2 3 4 5 6 7
jugadas: 7731631145444  (mueve jugador 2, ply 13)
óptimas reales: [6]   sin_D1 juega [2]   sin_D2 juega [7]   resultados por columna: {'1': 0, '2': -1, '3': 0, '4': 0, '5': 0, '6': 1, '7': -1}
```
```
. . . . . . .
. . . . . . .
. O . . . . O
. X . O . . X
. O . X . . X
. X X O O O X
1 2 3 4 5 6 7
jugadas: 22767444227735  (mueve jugador 1, ply 14)
óptimas reales: [5]   sin_D1 juega [4]   sin_D2 juega [1]   resultados por columna: {'1': -1, '2': -1, '3': -1, '4': -1, '5': 0, '6': -1, '7': -1}
```
```
. . . . . . .
. . . O . . .
X . . X . . .
O . . O . O .
O . . X . X O
O X . O X X X
1 2 3 4 5 6 7
jugadas: 7151276114444466  (mueve jugador 1, ply 16)
óptimas reales: [2]   sin_D1 juega [7]   sin_D2 juega [4]   resultados por columna: {'1': -1, '2': 1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1}
```

## D. Diversidad de las partidas por población (riesgo de colapso)

Solo jugadas de expertos. Entropía normalizada de la acción en estados visitados ≥3 veces (como Fig. 5 de [1]). Partidas únicas: fracción de transcripciones distintas.

| población | partidas | únicas | largo medio | estados visitados | visitados ≥3 | entropía media (≥3) | % tablas | % gana 1 |
|---|---|---|---|---|---|---|---|---|
| mix4h | 1500 | 1.000 | 21.3 | 21480 | 0 | nan | 1% | 56% |
