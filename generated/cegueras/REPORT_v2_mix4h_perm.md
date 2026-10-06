# Reporte v2_mix4h_perm (desempate: perm)

Estados decidibles analizados: 2301 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.306 | 0.245 | 0.330 (n=1173) | 0.313 (n=626) | 0.274 (n=339) | 0.166 (n=163) | 0.306 |
| sin_D2 | 0.299 | 0.245 | 0.335 (n=1173) | 0.307 (n=626) | 0.233 (n=339) | 0.141 (n=163) | 0.299 |
| sin_H | 0.302 | 0.248 | 0.337 (n=1173) | 0.294 (n=626) | 0.254 (n=339) | 0.190 (n=163) | 0.302 |
| sin_V | 0.215 | 0.177 | 0.239 (n=1173) | 0.241 (n=626) | 0.159 (n=339) | 0.061 (n=163) | 0.215 |
| sin_D1D2 | 0.318 | 0.258 | 0.317 (n=1173) | 0.359 (n=626) | 0.289 (n=339) | 0.221 (n=163) | 0.318 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.091 | 0.110 | 0.091 | 0.012 (n=254) |
| sin_D1 / sin_H | 0.044 | 0.102 | 0.092 | 0.098 (n=234) |
| sin_D1 / sin_V | 0.087 | 0.082 | 0.066 | 0.582 (n=189) |
| sin_D1 / sin_D1D2 | 0.275 | 0.156 | 0.097 | 0.178 (n=359) |
| sin_D2 / sin_H | 0.069 | 0.105 | 0.090 | 0.091 (n=241) |
| sin_D2 / sin_V | 0.035 | 0.071 | 0.064 | 0.172 (n=163) |
| sin_D2 / sin_D1D2 | 0.277 | 0.154 | 0.095 | 0.136 (n=354) |
| sin_H / sin_V | 0.005 | 0.066 | 0.065 | 0.118 (n=152) |
| sin_H / sin_D1D2 | 0.087 | 0.115 | 0.096 | 0.295 (n=264) |
| sin_V / sin_D1D2 | -0.014 | 0.066 | 0.068 | 0.073 (n=151) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.698 | 0.698 | 0.701 | -0.003 | 0.110 (n=254) | 0.136/0.117/0.050/0.025 |
| sin_D1 + sin_H | 0.696 | 0.696 | 0.698 | -0.002 | 0.102 (n=234) | 0.130/0.089/0.065/0.025 |
| sin_D1 + sin_V | 0.740 | 0.740 | 0.785 | -0.045 | 0.082 (n=189) | 0.100/0.086/0.047/0.012 |
| sin_D1 + sin_D1D2 | 0.688 | 0.688 | 0.694 | -0.006 | 0.156 (n=359) | 0.172/0.169/0.124/0.055 |
| sin_D2 + sin_H | 0.699 | 0.699 | 0.701 | -0.002 | 0.105 (n=241) | 0.134/0.096/0.065/0.012 |
| sin_D2 + sin_V | 0.743 | 0.743 | 0.785 | -0.042 | 0.071 (n=163) | 0.091/0.067/0.035/0.012 |
| sin_D2 + sin_D1D2 | 0.692 | 0.692 | 0.701 | -0.010 | 0.154 (n=354) | 0.169/0.179/0.100/0.061 |
| sin_H + sin_V | 0.741 | 0.741 | 0.785 | -0.044 | 0.066 (n=152) | 0.085/0.069/0.027/0.000 |
| sin_H + sin_D1D2 | 0.690 | 0.690 | 0.698 | -0.008 | 0.115 (n=264) | 0.130/0.125/0.088/0.018 |
| sin_V + sin_D1D2 | 0.734 | 0.734 | 0.785 | -0.051 | 0.066 (n=151) | 0.076/0.073/0.047/0.000 |
| sin_D1 + sin_D2 + sin_H | 0.698 | 0.767 | 0.701 | +0.065 | 0.046 (n=105) | 0.065/0.042/0.009/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.727 | 0.803 | 0.785 | +0.019 | 0.033 (n=77) | 0.048/0.032/0.003/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.693 | 0.732 | 0.701 | +0.031 | 0.068 (n=156) | 0.080/0.078/0.029/0.018 |
| sin_D1 + sin_H + sin_V | 0.726 | 0.805 | 0.785 | +0.020 | 0.030 (n=69) | 0.043/0.026/0.009/0.000 |
| sin_D1 + sin_H + sin_D1D2 | 0.691 | 0.754 | 0.698 | +0.057 | 0.058 (n=133) | 0.072/0.058/0.029/0.012 |
| sin_D1 + sin_V + sin_D1D2 | 0.721 | 0.788 | 0.785 | +0.003 | 0.042 (n=96) | 0.050/0.046/0.024/0.000 |
| sin_D2 + sin_H + sin_V | 0.728 | 0.808 | 0.785 | +0.023 | 0.029 (n=67) | 0.042/0.026/0.006/0.000 |
| sin_D2 + sin_H + sin_D1D2 | 0.694 | 0.754 | 0.701 | +0.052 | 0.059 (n=136) | 0.077/0.056/0.029/0.006 |
| sin_D2 + sin_V + sin_D1D2 | 0.723 | 0.787 | 0.785 | +0.002 | 0.038 (n=88) | 0.049/0.040/0.015/0.000 |
| sin_H + sin_V + sin_D1D2 | 0.722 | 0.798 | 0.785 | +0.013 | 0.025 (n=58) | 0.035/0.022/0.009/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.720 | 0.857 | 0.785 | +0.072 | 0.016 (n=37) | 0.026/0.011/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.694 | 0.799 | 0.701 | +0.098 | 0.028 (n=64) | 0.039/0.027/0.003/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.716 | 0.834 | 0.785 | +0.050 | 0.021 (n=49) | 0.029/0.022/0.003/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.715 | 0.840 | 0.785 | +0.055 | 0.017 (n=39) | 0.024/0.014/0.006/0.000 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.717 | 0.840 | 0.785 | +0.055 | 0.015 (n=35) | 0.024/0.010/0.003/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.712 | 0.874 | 0.785 | +0.090 | 0.010 (n=22) | 0.015/0.006/0.000/0.000 |

## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado

Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.

| conjunto | entropía media | estados con mezcla unánime |
|---|---|---|
| sin_D1 + sin_D2 | 0.305 | 0.191 |
| sin_D1 + sin_D2 + sin_H | 0.446 | 0.101 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.492 | 0.055 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.548 | 0.041 |

## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n=254 de 2301)

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
. . . O . . O
. . . X . . X
. . . O O . O
X X . O X . X
O O . X O O X
X X O X X O X
1 2 3 4 5 6 7
jugadas: 4356441571765477447517222  (mueve jugador 2, ply 25)
óptimas reales: [2, 3]   sin_D1 juega [1]   sin_D2 juega [6]   resultados por columna: {'1': -1, '2': 1, '3': 1, '5': -1, '6': -1}
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
óptimas reales: [5]   sin_D1 juega [4]   sin_D2 juega [7]   resultados por columna: {'1': -1, '2': -1, '3': -1, '4': -1, '5': 0, '6': -1, '7': -1}
```

## D. Diversidad de las partidas por población (riesgo de colapso)

Solo jugadas de expertos. Entropía normalizada de la acción en estados visitados ≥3 veces (como Fig. 5 de [1]). Partidas únicas: fracción de transcripciones distintas.

| población | partidas | únicas | largo medio | estados visitados | visitados ≥3 | entropía media (≥3) | % tablas | % gana 1 |
|---|---|---|---|---|---|---|---|---|
| mix4h | 1500 | 1.000 | 21.3 | 21480 | 0 | nan | 1% | 56% |
