# Reporte v1_mix5_perm (desempate: perm)

Estados decidibles analizados: 2238 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.241 | 0.201 | 0.246 (n=907) | 0.264 (n=774) | 0.211 (n=375) | 0.181 (n=182) | 0.241 |
| sin_D2 | 0.248 | 0.212 | 0.246 (n=907) | 0.253 (n=774) | 0.272 (n=375) | 0.187 (n=182) | 0.248 |
| sin_H | 0.311 | 0.266 | 0.420 (n=907) | 0.262 (n=774) | 0.219 (n=375) | 0.170 (n=182) | 0.311 |
| sin_V | 0.194 | 0.166 | 0.227 (n=907) | 0.222 (n=774) | 0.133 (n=375) | 0.038 (n=182) | 0.194 |
| sin_D1D2 | 0.365 | 0.315 | 0.324 (n=907) | 0.389 (n=774) | 0.400 (n=375) | 0.396 (n=182) | 0.365 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.030 | 0.065 | 0.060 | 0.055 (n=146) |
| sin_D1 / sin_H | 0.079 | 0.091 | 0.075 | 0.227 (n=203) |
| sin_D1 / sin_V | -0.002 | 0.046 | 0.047 | 0.135 (n=104) |
| sin_D1 / sin_D1D2 | 0.252 | 0.140 | 0.088 | 0.272 (n=313) |
| sin_D2 / sin_H | 0.166 | 0.110 | 0.077 | 0.628 (n=247) |
| sin_D2 / sin_V | 0.021 | 0.052 | 0.048 | 0.078 (n=116) |
| sin_D2 / sin_D1D2 | 0.435 | 0.181 | 0.091 | 0.714 (n=405) |
| sin_H / sin_V | -0.028 | 0.055 | 0.061 | 0.073 (n=124) |
| sin_H / sin_D1D2 | 0.157 | 0.149 | 0.114 | 0.652 (n=333) |
| sin_V / sin_D1D2 | -0.053 | 0.061 | 0.071 | 0.096 (n=136) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.756 | 0.756 | 0.759 | -0.004 | 0.065 (n=146) | 0.072/0.079/0.043/0.022 |
| sin_D1 + sin_H | 0.724 | 0.724 | 0.759 | -0.035 | 0.091 (n=203) | 0.132/0.075/0.056/0.022 |
| sin_D1 + sin_V | 0.782 | 0.782 | 0.806 | -0.023 | 0.046 (n=104) | 0.058/0.053/0.021/0.011 |
| sin_D1 + sin_D1D2 | 0.697 | 0.697 | 0.759 | -0.062 | 0.140 (n=313) | 0.130/0.154/0.136/0.137 |
| sin_D2 + sin_H | 0.720 | 0.720 | 0.752 | -0.032 | 0.110 (n=247) | 0.144/0.102/0.077/0.044 |
| sin_D2 + sin_V | 0.779 | 0.779 | 0.806 | -0.027 | 0.052 (n=116) | 0.058/0.059/0.043/0.005 |
| sin_D2 + sin_D1D2 | 0.693 | 0.693 | 0.752 | -0.059 | 0.181 (n=405) | 0.164/0.199/0.211/0.126 |
| sin_H + sin_V | 0.747 | 0.747 | 0.806 | -0.059 | 0.055 (n=124) | 0.076/0.056/0.024/0.016 |
| sin_H + sin_D1D2 | 0.662 | 0.662 | 0.689 | -0.027 | 0.149 (n=333) | 0.191/0.138/0.107/0.071 |
| sin_V + sin_D1D2 | 0.720 | 0.720 | 0.806 | -0.085 | 0.061 (n=136) | 0.058/0.079/0.051/0.016 |
| sin_D1 + sin_D2 + sin_H | 0.733 | 0.809 | 0.759 | +0.050 | 0.037 (n=83) | 0.051/0.035/0.027/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.772 | 0.859 | 0.806 | +0.054 | 0.013 (n=30) | 0.018/0.017/0.003/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.715 | 0.738 | 0.759 | -0.022 | 0.057 (n=127) | 0.058/0.070/0.043/0.022 |
| sin_D1 + sin_H + sin_V | 0.751 | 0.843 | 0.806 | +0.037 | 0.020 (n=44) | 0.031/0.016/0.008/0.005 |
| sin_D1 + sin_H + sin_D1D2 | 0.694 | 0.763 | 0.759 | +0.004 | 0.067 (n=149) | 0.088/0.061/0.053/0.011 |
| sin_D1 + sin_V + sin_D1D2 | 0.733 | 0.805 | 0.806 | -0.001 | 0.022 (n=50) | 0.024/0.028/0.013/0.005 |
| sin_D2 + sin_H + sin_V | 0.749 | 0.823 | 0.806 | +0.017 | 0.022 (n=50) | 0.030/0.025/0.008/0.005 |
| sin_D2 + sin_H + sin_D1D2 | 0.692 | 0.714 | 0.752 | -0.038 | 0.079 (n=177) | 0.100/0.076/0.059/0.027 |
| sin_D2 + sin_V + sin_D1D2 | 0.731 | 0.776 | 0.806 | -0.030 | 0.034 (n=77) | 0.035/0.045/0.027/0.000 |
| sin_H + sin_V + sin_D1D2 | 0.710 | 0.787 | 0.806 | -0.019 | 0.029 (n=66) | 0.034/0.037/0.013/0.005 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.751 | 0.886 | 0.806 | +0.080 | 0.009 (n=21) | 0.014/0.009/0.003/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.709 | 0.776 | 0.759 | +0.017 | 0.033 (n=74) | 0.043/0.032/0.027/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.738 | 0.824 | 0.806 | +0.018 | 0.009 (n=21) | 0.012/0.012/0.003/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.722 | 0.846 | 0.806 | +0.040 | 0.014 (n=31) | 0.019/0.014/0.008/0.000 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.720 | 0.794 | 0.806 | -0.012 | 0.017 (n=38) | 0.020/0.023/0.005/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.728 | 0.849 | 0.806 | +0.043 | 0.008 (n=17) | 0.011/0.008/0.003/0.000 |

## C2. Diversidad de acciones: entropía normalizada de la mezcla por estado

Entropía (base 2) de la distribución de jugadas de la mezcla equiponderada, dividida por log2(#legales); promedio sobre estados decidibles.

| conjunto | entropía media | estados con mezcla unánime |
|---|---|---|
| sin_D1 + sin_D2 | 0.282 | 0.258 |
| sin_D1 + sin_D2 + sin_H | 0.362 | 0.135 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.454 | 0.069 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.474 | 0.045 |

## C3. Ejemplos de estados donde sin_D1 y sin_D2 erran ambos (n=146 de 2238)

```
. O . . . . .
. X . . . . .
. X X . . . X
. O O X . . O
O O O X O X O
X X X O X X O
1 2 3 4 5 6 7
jugadas: 22625724334327621137754  (mueve jugador 2, ply 23)
óptimas reales: [3]   sin_D1 juega [5]   sin_D2 juega [4]   resultados por columna: {'1': 0, '3': 1, '4': 0, '5': -1, '6': -1, '7': -1}
```
```
O . . . . X .
X . . . X O .
O . . . O O .
X . X . O X .
O . X . O X .
X O O O X X X
1 2 3 4 5 6 7
jugadas: 63341112556566355116716  (mueve jugador 2, ply 23)
óptimas reales: [4]   sin_D1 juega [2]   sin_D2 juega [3]   resultados por columna: {'2': -1, '3': -1, '4': 1, '5': -1, '7': -1}
```
```
. . . . . . .
. . . O . . .
. O . X . . .
. O . X O . .
. X . O X . X
O X . X O X O
1 2 3 4 5 6 7
jugadas: 4467452144552272  (mueve jugador 1, ply 16)
óptimas reales: [1, 7]   sin_D1 juega [5]   sin_D2 juega [6]   resultados por columna: {'1': 1, '2': -1, '3': -1, '4': -1, '5': -1, '6': -1, '7': 1}
```
```
. . . . . . .
. . O . . . .
. . X . . . .
. . X . . . .
. . X . . O O
X O O X . O X
1 2 3 4 5 6 7
jugadas: 731237463633  (mueve jugador 1, ply 12)
óptimas reales: [2, 4]   sin_D1 juega [5]   sin_D2 juega [6]   resultados por columna: {'1': -1, '2': 1, '3': -1, '4': 1, '5': -1, '6': -1, '7': -1}
```
