# Reporte v1_mix5

Estados decidibles analizados: 2238 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.262 | 0.221 | 0.254 (n=907) | 0.281 (n=774) | 0.255 (n=375) | 0.235 (n=182) | 0.021 |
| sin_D2 | 0.253 | 0.214 | 0.255 (n=907) | 0.256 (n=774) | 0.265 (n=375) | 0.206 (n=182) | 0.027 |
| sin_H | 0.317 | 0.267 | 0.415 (n=907) | 0.268 (n=774) | 0.232 (n=375) | 0.221 (n=182) | 0.053 |
| sin_V | 0.197 | 0.169 | 0.235 (n=907) | 0.219 (n=774) | 0.135 (n=375) | 0.042 (n=182) | 0.019 |
| sin_D1D2 | 0.359 | 0.308 | 0.324 (n=907) | 0.385 (n=774) | 0.369 (n=375) | 0.408 (n=182) | 0.043 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.130 | 0.002 | 0.001 | 0.062 (n=4) |
| sin_D1 / sin_H | 0.131 | 0.002 | 0.001 | 0.083 (n=4) |
| sin_D1 / sin_V | 0.037 | 0.000 | 0.000 | 0.500 (n=1) |
| sin_D1 / sin_D1D2 | 0.504 | 0.005 | 0.001 | 0.750 (n=12) |
| sin_D2 / sin_H | 0.124 | 0.002 | 0.001 | 0.183 (n=5) |
| sin_D2 / sin_V | 0.046 | 0.002 | 0.001 | 0.417 (n=4) |
| sin_D2 / sin_D1D2 | 0.471 | 0.005 | 0.001 | 0.778 (n=12) |
| sin_H / sin_V | 0.010 | 0.000 | 0.001 | nan (n=0) |
| sin_H / sin_D1D2 | 0.052 | 0.003 | 0.002 | 0.167 (n=6) |
| sin_V / sin_D1D2 | -0.035 | 0.000 | 0.001 | 0.000 (n=1) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.742 | 0.883 | 0.747 | +0.136 | 0.002 (n=4) | 0.003/0.001/0.000/0.000 |
| sin_D1 + sin_H | 0.710 | 0.854 | 0.738 | +0.117 | 0.002 (n=4) | 0.004/0.000/0.000/0.000 |
| sin_D1 + sin_V | 0.770 | 0.914 | 0.803 | +0.111 | 0.000 (n=1) | 0.000/0.001/0.000/0.000 |
| sin_D1 + sin_D1D2 | 0.689 | 0.779 | 0.738 | +0.042 | 0.005 (n=12) | 0.007/0.003/0.005/0.011 |
| sin_D2 + sin_H | 0.715 | 0.857 | 0.747 | +0.110 | 0.002 (n=5) | 0.004/0.001/0.000/0.000 |
| sin_D2 + sin_V | 0.775 | 0.913 | 0.803 | +0.111 | 0.002 (n=4) | 0.002/0.003/0.000/0.000 |
| sin_D2 + sin_D1D2 | 0.694 | 0.791 | 0.747 | +0.044 | 0.005 (n=12) | 0.004/0.008/0.005/0.000 |
| sin_H + sin_V | 0.743 | 0.897 | 0.803 | +0.094 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_H + sin_D1D2 | 0.662 | 0.821 | 0.683 | +0.138 | 0.003 (n=6) | 0.003/0.004/0.000/0.000 |
| sin_V + sin_D1D2 | 0.722 | 0.893 | 0.803 | +0.091 | 0.000 (n=1) | 0.000/0.001/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H | 0.722 | 0.923 | 0.747 | +0.176 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_V | 0.763 | 0.948 | 0.803 | +0.145 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.709 | 0.882 | 0.747 | +0.135 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_H + sin_V | 0.741 | 0.939 | 0.803 | +0.136 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_H + sin_D1D2 | 0.687 | 0.880 | 0.738 | +0.142 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_V + sin_D1D2 | 0.727 | 0.921 | 0.803 | +0.118 | 0.000 (n=1) | 0.000/0.001/0.000/0.000 |
| sin_D2 + sin_H + sin_V | 0.744 | 0.943 | 0.803 | +0.140 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D2 + sin_H + sin_D1D2 | 0.690 | 0.884 | 0.747 | +0.137 | 0.001 (n=2) | 0.001/0.001/0.000/0.000 |
| sin_D2 + sin_V + sin_D1D2 | 0.730 | 0.921 | 0.803 | +0.118 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_H + sin_V + sin_D1D2 | 0.709 | 0.935 | 0.803 | +0.132 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.743 | 0.958 | 0.803 | +0.155 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.702 | 0.923 | 0.747 | +0.176 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.732 | 0.945 | 0.803 | +0.143 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.716 | 0.944 | 0.803 | +0.142 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.718 | 0.949 | 0.803 | +0.146 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.722 | 0.957 | 0.803 | +0.154 | 0.000 (n=0) | 0.000/0.000/0.000/0.000 |

## D. Diversidad de las partidas por población (riesgo de colapso)

Solo jugadas de expertos. Entropía normalizada de la acción en estados visitados ≥3 veces (como Fig. 5 de [1]). Partidas únicas: fracción de transcripciones distintas.

| población | partidas | únicas | largo medio | estados visitados | visitados ≥3 | entropía media (≥3) | % tablas | % gana 1 |
|---|---|---|---|---|---|---|---|---|
| mix5 | 1500 | 1.000 | 20.5 | 15984 | 0 | nan | 1% | 58% |
| self_sinD1 | 400 | 1.000 | 20.8 | 4358 | 0 | nan | 3% | 56% |
| self_sinD2 | 400 | 1.000 | 20.9 | 4391 | 0 | nan | 4% | 52% |
| self_sinH | 400 | 1.000 | 23.7 | 5556 | 0 | nan | 6% | 48% |
| self_sinV | 400 | 1.000 | 21.4 | 4626 | 0 | nan | 5% | 56% |

## E. Fuerza relativa (round robin, puntos de la fila contra la columna: W=1, D=½, mismas aperturas, ambos colores)

| | optimo | sin_D1 | sin_D2 | sin_H | sin_V | sin_D1D2 | random | promedio |
|---|---|---|---|---|---|---|---|---|
| **optimo** | 0.50 | 0.63 | 0.70 | 0.69 | 0.74 | 0.65 | 0.91 | 0.69 |
| **sin_D1** | 0.37 | 0.50 | 0.48 | 0.57 | 0.54 | 0.60 | 0.87 | 0.56 |
| **sin_D2** | 0.30 | 0.52 | 0.50 | 0.59 | 0.54 | 0.61 | 0.83 | 0.56 |
| **sin_H** | 0.31 | 0.43 | 0.41 | 0.50 | 0.47 | 0.49 | 0.80 | 0.49 |
| **sin_V** | 0.26 | 0.46 | 0.46 | 0.53 | 0.50 | 0.48 | 0.83 | 0.50 |
| **sin_D1D2** | 0.35 | 0.40 | 0.39 | 0.51 | 0.52 | 0.50 | 0.85 | 0.50 |
| **random** | 0.09 | 0.13 | 0.17 | 0.20 | 0.17 | 0.15 | 0.50 | 0.20 |
