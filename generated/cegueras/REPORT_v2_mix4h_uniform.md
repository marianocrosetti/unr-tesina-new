# Reporte v2_mix4h_uniform (desempate: uniform)

Estados decidibles analizados: 2301 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.266 | 0.215 | 0.273 (n=1173) | 0.282 (n=626) | 0.252 (n=339) | 0.182 (n=163) | 0.029 |
| sin_D2 | 0.262 | 0.212 | 0.275 (n=1173) | 0.276 (n=626) | 0.241 (n=339) | 0.160 (n=163) | 0.030 |
| sin_H | 0.364 | 0.295 | 0.446 (n=1173) | 0.306 (n=626) | 0.257 (n=339) | 0.217 (n=163) | 0.048 |
| sin_V | 0.196 | 0.165 | 0.207 (n=1173) | 0.231 (n=626) | 0.162 (n=339) | 0.063 (n=163) | 0.025 |
| sin_D1D2 | 0.342 | 0.279 | 0.349 (n=1173) | 0.364 (n=626) | 0.332 (n=339) | 0.236 (n=163) | 0.057 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.183 | 0.005 | 0.001 | 0.281 (n=12) |
| sin_D1 / sin_H | 0.137 | 0.004 | 0.001 | 0.267 (n=10) |
| sin_D1 / sin_V | 0.080 | 0.004 | 0.001 | 0.426 (n=9) |
| sin_D1 / sin_D1D2 | 0.522 | 0.009 | 0.002 | 0.567 (n=21) |
| sin_D2 / sin_H | 0.232 | 0.004 | 0.001 | 0.222 (n=9) |
| sin_D2 / sin_V | 0.067 | 0.003 | 0.001 | 0.357 (n=7) |
| sin_D2 / sin_D1D2 | 0.521 | 0.010 | 0.002 | 0.659 (n=22) |
| sin_H / sin_V | -0.046 | 0.002 | 0.001 | 0.300 (n=5) |
| sin_H / sin_D1D2 | 0.162 | 0.004 | 0.003 | 0.241 (n=9) |
| sin_V / sin_D1D2 | -0.010 | 0.002 | 0.001 | 0.167 (n=4) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.736 | 0.870 | 0.738 | +0.133 | 0.005 (n=12) | 0.009/0.002/0.000/0.000 |
| sin_D1 + sin_H | 0.685 | 0.835 | 0.734 | +0.101 | 0.004 (n=10) | 0.006/0.005/0.000/0.000 |
| sin_D1 + sin_V | 0.769 | 0.908 | 0.804 | +0.105 | 0.004 (n=9) | 0.006/0.003/0.000/0.000 |
| sin_D1 + sin_D1D2 | 0.696 | 0.777 | 0.734 | +0.043 | 0.009 (n=21) | 0.010/0.008/0.009/0.006 |
| sin_D2 + sin_H | 0.687 | 0.826 | 0.738 | +0.088 | 0.004 (n=9) | 0.007/0.002/0.000/0.000 |
| sin_D2 + sin_V | 0.771 | 0.909 | 0.804 | +0.106 | 0.003 (n=7) | 0.006/0.000/0.000/0.000 |
| sin_D2 + sin_D1D2 | 0.698 | 0.784 | 0.738 | +0.046 | 0.010 (n=22) | 0.009/0.013/0.006/0.006 |
| sin_H + sin_V | 0.720 | 0.894 | 0.804 | +0.090 | 0.002 (n=5) | 0.003/0.003/0.000/0.000 |
| sin_H + sin_D1D2 | 0.647 | 0.784 | 0.658 | +0.127 | 0.004 (n=9) | 0.006/0.003/0.000/0.000 |
| sin_V + sin_D1D2 | 0.731 | 0.889 | 0.804 | +0.085 | 0.002 (n=4) | 0.003/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H | 0.703 | 0.903 | 0.738 | +0.166 | 0.001 (n=3) | 0.002/0.002/0.000/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.759 | 0.943 | 0.804 | +0.140 | 0.001 (n=3) | 0.003/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.710 | 0.866 | 0.738 | +0.128 | 0.002 (n=5) | 0.003/0.002/0.000/0.000 |
| sin_D1 + sin_H + sin_V | 0.725 | 0.937 | 0.804 | +0.134 | 0.001 (n=3) | 0.001/0.003/0.000/0.000 |
| sin_D1 + sin_H + sin_D1D2 | 0.676 | 0.857 | 0.734 | +0.123 | 0.001 (n=2) | 0.001/0.002/0.000/0.000 |
| sin_D1 + sin_V + sin_D1D2 | 0.732 | 0.915 | 0.804 | +0.111 | 0.001 (n=2) | 0.002/0.000/0.000/0.000 |
| sin_D2 + sin_H + sin_V | 0.726 | 0.932 | 0.804 | +0.128 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D2 + sin_H + sin_D1D2 | 0.677 | 0.851 | 0.738 | +0.113 | 0.001 (n=2) | 0.001/0.002/0.000/0.000 |
| sin_D2 + sin_V + sin_D1D2 | 0.733 | 0.910 | 0.804 | +0.106 | 0.001 (n=3) | 0.003/0.000/0.000/0.000 |
| sin_H + sin_V + sin_D1D2 | 0.699 | 0.923 | 0.804 | +0.119 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.728 | 0.951 | 0.804 | +0.147 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.691 | 0.898 | 0.738 | +0.160 | 0.000 (n=1) | 0.000/0.002/0.000/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.733 | 0.931 | 0.804 | +0.128 | 0.000 (n=1) | 0.001/0.000/0.000/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.708 | 0.937 | 0.804 | +0.133 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.709 | 0.932 | 0.804 | +0.128 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.714 | 0.944 | 0.804 | +0.140 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |

## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado

Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.

| conjunto | entropía media | estados con mezcla unánime |
|---|---|---|
| sin_D1 + sin_D2 | 0.647 | 0.116 |
| sin_D1 + sin_D2 + sin_H | 0.731 | 0.044 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.742 | 0.009 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.753 | 0.007 |

## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n=12 de 2301)

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
. . . O . . .
. . X X O . .
. O O X O . .
. O X O X X X
1 2 3 4 5 6 7
jugadas: 32536472454435  (mueve jugador 1, ply 14)
óptimas reales: [4]   sin_D1 juega [2]   sin_D2 juega [3, 6]   resultados por columna: {'1': -1, '2': 0, '3': 0, '4': 1, '5': 0, '6': 0, '7': -1}
```
```
. . . . . . .
. O . . . . .
. X X . . . .
. X O . . . .
. X O O . . O
O O X X X O X
1 2 3 4 5 6 7
jugadas: 7221374356232234  (mueve jugador 1, ply 16)
óptimas reales: [6]   sin_D1 juega [4]   sin_D2 juega [3, 5]   resultados por columna: {'1': -1, '2': -1, '3': -1, '4': 0, '5': 0, '6': 1, '7': -1}
```
```
. . . . . . .
X . . . . . .
O . . O . . .
O . . X . . .
O . . X . . .
X X . O . X O
1 2 3 4 5 6 7
jugadas: 146741412114  (mueve jugador 1, ply 12)
óptimas reales: [6]   sin_D1 juega [1, 3, 4, 5, 7]   sin_D2 juega [4]   resultados por columna: {'1': -1, '2': -1, '3': -1, '4': 0, '5': -1, '6': 1, '7': -1}
```

## D. Diversidad de las partidas por población (riesgo de colapso)

Solo jugadas de expertos. Entropía normalizada de la acción en estados visitados ≥3 veces (como Fig. 5 de [1]). Partidas únicas: fracción de transcripciones distintas.

| población | partidas | únicas | largo medio | estados visitados | visitados ≥3 | entropía media (≥3) | % tablas | % gana 1 |
|---|---|---|---|---|---|---|---|---|
| mix4h | 1500 | 1.000 | 21.3 | 21480 | 0 | nan | 1% | 56% |
