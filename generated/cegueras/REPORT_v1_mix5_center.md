# Reporte v1_mix5_center (desempate: center)

Estados decidibles analizados: 2238 (de partidas con apertura aleatoria; solo jugadas de expertos).

## A. Tasa de error estructural por experto (prob. de jugar no óptimo en un estado decidible)

Tasa = 1 − |óptimas_variante ∩ óptimas_reales| / |óptimas_variante|. Pérdida = recompensa óptima − recompensa esperada de la jugada (1/½/0).

| experto | tasa total | pérdida media | tasa 8-14 | tasa 15-21 | tasa 22-28 | tasa 29+ | error seguro (∩=∅) |
|---|---|---|---|---|---|---|---|
| sin_D1 | 0.228 | 0.188 | 0.203 (n=907) | 0.242 (n=774) | 0.261 (n=375) | 0.225 (n=182) | 0.228 |
| sin_D2 | 0.205 | 0.168 | 0.206 (n=907) | 0.208 (n=774) | 0.224 (n=375) | 0.143 (n=182) | 0.205 |
| sin_H | 0.273 | 0.227 | 0.344 (n=907) | 0.227 (n=774) | 0.237 (n=375) | 0.187 (n=182) | 0.273 |
| sin_V | 0.193 | 0.164 | 0.238 (n=907) | 0.202 (n=774) | 0.141 (n=375) | 0.038 (n=182) | 0.193 |
| sin_D1D2 | 0.308 | 0.261 | 0.257 (n=907) | 0.341 (n=774) | 0.344 (n=375) | 0.346 (n=182) | 0.308 |

## B. Correlación de errores entre pares de expertos

Pearson entre los vectores de tasa de error por estado; P(ambos erran seguro); Jaccard de las jugadas erróneas cuando ambos erran.

| par | Pearson | P(ambos erran) | P(ambos) si indep. | Jaccard jugadas erróneas |
|---|---|---|---|---|
| sin_D1 / sin_D2 | 0.216 | 0.083 | 0.047 | 0.758 (n=186) |
| sin_D1 / sin_H | 0.258 | 0.110 | 0.062 | 0.704 (n=247) |
| sin_D1 / sin_V | 0.161 | 0.071 | 0.044 | 0.766 (n=158) |
| sin_D1 / sin_D1D2 | 0.588 | 0.184 | 0.070 | 0.840 (n=412) |
| sin_D2 / sin_H | 0.234 | 0.098 | 0.056 | 0.694 (n=219) |
| sin_D2 / sin_V | 0.212 | 0.073 | 0.040 | 0.762 (n=164) |
| sin_D2 / sin_D1D2 | 0.458 | 0.148 | 0.063 | 0.816 (n=332) |
| sin_H / sin_V | 0.163 | 0.081 | 0.053 | 0.731 (n=182) |
| sin_H / sin_D1D2 | 0.232 | 0.132 | 0.084 | 0.685 (n=295) |
| sin_V / sin_D1D2 | 0.155 | 0.088 | 0.059 | 0.714 (n=196) |

## C. Techo del voto (Proposición 2 de [1]) por conjunto de expertos

acc(argmax mezcla) = tasa de acierto de la jugada más probable de la mezcla equiponderada (τ→0); acc(τ=1) = masa de la mezcla sobre jugadas óptimas; mejor experto = mayor acc individual. Trascendencia por voto posible si argmax > mejor experto.

| conjunto | acc τ=1 | acc argmax (τ→0) | mejor experto | ganancia argmax − mejor | estados donde todos erran seguro | ídem por fase 8-14/15-21/22-28/29+ |
|---|---|---|---|---|---|---|
| sin_D1 + sin_D2 | 0.784 | 0.784 | 0.795 | -0.012 | 0.083 (n=186) | 0.085/0.088/0.096/0.027 |
| sin_D1 + sin_H | 0.750 | 0.750 | 0.772 | -0.023 | 0.110 (n=247) | 0.127/0.102/0.120/0.044 |
| sin_D1 + sin_V | 0.790 | 0.790 | 0.807 | -0.017 | 0.071 (n=158) | 0.088/0.075/0.048/0.011 |
| sin_D1 + sin_D1D2 | 0.732 | 0.732 | 0.772 | -0.040 | 0.184 (n=412) | 0.151/0.199/0.221/0.209 |
| sin_D2 + sin_H | 0.761 | 0.761 | 0.795 | -0.034 | 0.098 (n=219) | 0.123/0.084/0.088/0.049 |
| sin_D2 + sin_V | 0.801 | 0.801 | 0.807 | -0.006 | 0.073 (n=164) | 0.103/0.066/0.051/0.005 |
| sin_D2 + sin_D1D2 | 0.744 | 0.744 | 0.795 | -0.052 | 0.148 (n=332) | 0.137/0.163/0.168/0.104 |
| sin_H + sin_V | 0.767 | 0.767 | 0.807 | -0.040 | 0.081 (n=182) | 0.117/0.068/0.053/0.016 |
| sin_H + sin_D1D2 | 0.710 | 0.710 | 0.727 | -0.017 | 0.132 (n=295) | 0.151/0.121/0.123/0.099 |
| sin_V + sin_D1D2 | 0.750 | 0.750 | 0.807 | -0.057 | 0.088 (n=196) | 0.107/0.097/0.053/0.022 |
| sin_D1 + sin_D2 + sin_H | 0.765 | 0.813 | 0.795 | +0.017 | 0.050 (n=111) | 0.060/0.044/0.059/0.005 |
| sin_D1 + sin_D2 + sin_V | 0.791 | 0.841 | 0.807 | +0.034 | 0.033 (n=73) | 0.043/0.035/0.019/0.000 |
| sin_D1 + sin_D2 + sin_D1D2 | 0.753 | 0.735 | 0.795 | -0.060 | 0.074 (n=166) | 0.075/0.079/0.085/0.027 |
| sin_D1 + sin_H + sin_V | 0.769 | 0.823 | 0.807 | +0.016 | 0.042 (n=94) | 0.060/0.037/0.027/0.005 |
| sin_D1 + sin_H + sin_D1D2 | 0.730 | 0.752 | 0.772 | -0.020 | 0.088 (n=197) | 0.101/0.078/0.101/0.038 |
| sin_D1 + sin_V + sin_D1D2 | 0.757 | 0.771 | 0.807 | -0.036 | 0.055 (n=123) | 0.062/0.066/0.037/0.011 |
| sin_D2 + sin_H + sin_V | 0.776 | 0.829 | 0.807 | +0.022 | 0.039 (n=88) | 0.062/0.030/0.021/0.005 |
| sin_D2 + sin_H + sin_D1D2 | 0.738 | 0.764 | 0.795 | -0.031 | 0.070 (n=157) | 0.083/0.066/0.064/0.038 |
| sin_D2 + sin_V + sin_D1D2 | 0.765 | 0.804 | 0.807 | -0.003 | 0.055 (n=124) | 0.076/0.054/0.032/0.005 |
| sin_H + sin_V + sin_D1D2 | 0.742 | 0.796 | 0.807 | -0.011 | 0.047 (n=106) | 0.068/0.040/0.027/0.016 |
| sin_D1 + sin_D2 + sin_H + sin_V | 0.775 | 0.836 | 0.807 | +0.029 | 0.023 (n=52) | 0.033/0.022/0.013/0.000 |
| sin_D1 + sin_D2 + sin_H + sin_D1D2 | 0.747 | 0.764 | 0.795 | -0.031 | 0.043 (n=97) | 0.053/0.037/0.051/0.005 |
| sin_D1 + sin_D2 + sin_V + sin_D1D2 | 0.767 | 0.789 | 0.807 | -0.018 | 0.029 (n=66) | 0.039/0.032/0.016/0.000 |
| sin_D1 + sin_H + sin_V + sin_D1D2 | 0.750 | 0.792 | 0.807 | -0.015 | 0.033 (n=74) | 0.045/0.031/0.021/0.005 |
| sin_D2 + sin_H + sin_V + sin_D1D2 | 0.755 | 0.804 | 0.807 | -0.003 | 0.031 (n=69) | 0.046/0.026/0.016/0.005 |
| sin_D1 + sin_D2 + sin_H + sin_V + sin_D1D2 | 0.759 | 0.813 | 0.807 | +0.006 | 0.020 (n=45) | 0.029/0.019/0.011/0.000 |
