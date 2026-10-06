# Reporte v1_mix5_hash (desempate: hash)

Estados decidibles analizados: 2238 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.259 | 0.219 | 0.247 (n=907) | 0.279 (n=774) | 0.272 (n=375) | 0.209 (n=182) | 0.259 |
| sin_D2 | 0.243 | 0.204 | 0.246 (n=907) | 0.224 (n=774) | 0.283 (n=375) | 0.225 (n=182) | 0.243 |
| sin_H | 0.322 | 0.269 | 0.422 (n=907) | 0.262 (n=774) | 0.256 (n=375) | 0.214 (n=182) | 0.322 |
| sin_V | 0.206 | 0.178 | 0.237 (n=907) | 0.238 (n=774) | 0.149 (n=375) | 0.038 (n=182) | 0.206 |
| sin_D1D2 | 0.355 | 0.303 | 0.332 (n=907) | 0.394 (n=774) | 0.312 (n=375) | 0.390 (n=182) | 0.355 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.082 | 0.078 | 0.063 | 0.183 (n=175) |
| sin_D1 / sin_H | 0.079 | 0.100 | 0.083 | 0.215 (n=223) |
| sin_D1 / sin_V | 0.041 | 0.061 | 0.053 | 0.250 (n=136) |
| sin_D1 / sin_D1D2 | 0.301 | 0.155 | 0.092 | 0.256 (n=347) |
| sin_D2 / sin_H | 0.049 | 0.088 | 0.078 | 0.218 (n=197) |
| sin_D2 / sin_V | 0.038 | 0.057 | 0.050 | 0.291 (n=127) |
| sin_D2 / sin_D1D2 | 0.260 | 0.139 | 0.086 | 0.285 (n=312) |
| sin_H / sin_V | 0.000 | 0.067 | 0.067 | 0.221 (n=149) |
| sin_H / sin_D1D2 | 0.036 | 0.122 | 0.114 | 0.259 (n=274) |
| sin_V / sin_D1D2 | -0.030 | 0.067 | 0.073 | 0.265 (n=151) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.749 | 0.749 | 0.757 | -0.008 | 0.078 (n=175) | 0.092/0.070/0.088/0.027 |
| sin_D1 + sin_H | 0.709 | 0.709 | 0.741 | -0.032 | 0.100 (n=223) | 0.141/0.080/0.080/0.016 |
| sin_D1 + sin_V | 0.767 | 0.767 | 0.794 | -0.026 | 0.061 (n=136) | 0.069/0.074/0.037/0.011 |
| sin_D1 + sin_D1D2 | 0.693 | 0.693 | 0.741 | -0.048 | 0.155 (n=347) | 0.143/0.171/0.157/0.143 |
| sin_D2 + sin_H | 0.718 | 0.718 | 0.757 | -0.040 | 0.088 (n=197) | 0.120/0.066/0.080/0.038 |
| sin_D2 + sin_V | 0.775 | 0.775 | 0.794 | -0.018 | 0.057 (n=127) | 0.068/0.062/0.040/0.011 |
| sin_D2 + sin_D1D2 | 0.701 | 0.701 | 0.757 | -0.056 | 0.139 (n=312) | 0.136/0.145/0.147/0.121 |
| sin_H + sin_V | 0.736 | 0.736 | 0.794 | -0.058 | 0.067 (n=149) | 0.089/0.066/0.037/0.016 |
| sin_H + sin_D1D2 | 0.662 | 0.662 | 0.678 | -0.016 | 0.122 (n=274) | 0.170/0.105/0.077/0.055 |
| sin_V + sin_D1D2 | 0.719 | 0.719 | 0.794 | -0.074 | 0.067 (n=151) | 0.069/0.089/0.037/0.027 |
| sin_D1 + sin_D2 + sin_H | 0.725 | 0.808 | 0.757 | +0.050 | 0.035 (n=79) | 0.053/0.025/0.032/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.764 | 0.848 | 0.794 | +0.055 | 0.024 (n=53) | 0.029/0.030/0.011/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.714 | 0.756 | 0.757 | -0.001 | 0.057 (n=127) | 0.066/0.053/0.059/0.022 |
| sin_D1 + sin_H + sin_V | 0.737 | 0.824 | 0.794 | +0.030 | 0.029 (n=64) | 0.042/0.026/0.013/0.005 |
| sin_D1 + sin_H + sin_D1D2 | 0.688 | 0.752 | 0.741 | +0.011 | 0.059 (n=133) | 0.083/0.050/0.045/0.011 |
| sin_D1 + sin_V + sin_D1D2 | 0.727 | 0.795 | 0.794 | +0.002 | 0.036 (n=81) | 0.035/0.049/0.024/0.011 |
| sin_D2 + sin_H + sin_V | 0.743 | 0.829 | 0.794 | +0.036 | 0.023 (n=52) | 0.033/0.023/0.008/0.005 |
| sin_D2 + sin_H + sin_D1D2 | 0.693 | 0.761 | 0.757 | +0.003 | 0.052 (n=117) | 0.069/0.045/0.043/0.016 |
| sin_D2 + sin_V + sin_D1D2 | 0.732 | 0.801 | 0.794 | +0.008 | 0.034 (n=76) | 0.039/0.044/0.016/0.005 |
| sin_H + sin_V + sin_D1D2 | 0.706 | 0.794 | 0.794 | +0.000 | 0.028 (n=63) | 0.036/0.028/0.013/0.016 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.742 | 0.884 | 0.794 | +0.090 | 0.013 (n=29) | 0.018/0.016/0.003/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.705 | 0.820 | 0.757 | +0.062 | 0.027 (n=61) | 0.040/0.022/0.021/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.734 | 0.852 | 0.794 | +0.058 | 0.019 (n=42) | 0.022/0.025/0.008/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.714 | 0.844 | 0.794 | +0.051 | 0.017 (n=39) | 0.023/0.017/0.011/0.005 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.718 | 0.849 | 0.794 | +0.055 | 0.016 (n=35) | 0.020/0.018/0.005/0.005 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.723 | 0.883 | 0.794 | +0.090 | 0.011 (n=24) | 0.013/0.014/0.003/0.000 |

## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado

Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.

| conjunto | entropía media | estados con mezcla unánime |
|---|---|---|
| sin_D1 + sin_D2 | 0.262 | 0.317 |
| sin_D1 + sin_D2 + sin_H | 0.398 | 0.123 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.463 | 0.064 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.521 | 0.037 |

## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n=175 de 2238)

```
. . . . . . .
. . O . . . .
. . X . . . .
. . X . . . .
. . X . . O O
X O O X . O X
1 2 3 4 5 6 7
jugadas: 731237463633  (mueve jugador 1, ply 12)
óptimas reales: [2, 4]   sin_D1 juega [1]   sin_D2 juega [5]   resultados por columna: {'1': -1, '2': 1, '3': -1, '4': 1, '5': -1, '6': -1, '7': -1}
```
```
. . . . . . .
. . . . . . .
. . . . . . .
. . . . . . O
O . O O X X X
X X O X O X O
1 2 3 4 5 6 7
jugadas: 17234561536477  (mueve jugador 1, ply 14)
óptimas reales: [2]   sin_D1 juega [5]   sin_D2 juega [6]   resultados por columna: {'1': -1, '2': 1, '3': -1, '4': -1, '5': -1, '6': -1, '7': -1}
```
```
. . . . . . .
. . . . . . .
O . . . . . .
X . . . . O X
X . . X . O O
X X . O O X O
1 2 3 4 5 6 7
jugadas: 65172774161146  (mueve jugador 1, ply 14)
óptimas reales: [6]   sin_D1 juega [1]   sin_D2 juega [2]   resultados por columna: {'1': -1, '2': -1, '3': -1, '4': -1, '5': -1, '6': 0, '7': -1}
```
```
. . . . . . .
. . . X . . .
. . . X O . O
X . O O X . X
O . X O X O X
O . X O O X X
1 2 3 4 5 6 7
jugadas: 663475745441513315774  (mueve jugador 2, ply 21)
óptimas reales: [3, 5]   sin_D1 juega [4]   sin_D2 juega [4]   resultados por columna: {'1': -1, '2': -1, '3': 1, '4': -1, '5': 1, '6': -1, '7': -1}
```
