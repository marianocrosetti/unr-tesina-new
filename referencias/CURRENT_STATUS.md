Estos son los dos pappers principales en los que nos basamos:
[1] - abreu2025_taxonomy_of_transcendence.pdf
[2] - zhang2024_transcendence.pdf

TODO:

- Cuando estemos redactando vamos a revisar esta bibliografía para considerar añadirla:
<AI-CONTENT-NOT-CURATED>
### Imprescindibles (sostienen el objetivo 5 como pregunta abierta)

- A. Mészáros, P. Reizinger, F. Huszár. *Out-of-distribution Tests Reveal Compositionality in Chess Transformers*. arXiv:2510.20783, 2025. (Bando optimista: composición en transformers de ajedrez, verificado el ID.)
- K. Paster, S. McIlraith, J. Ba. *You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments*. NeurIPS, 2022. (Bando pesimista.)
- D. Brandfonbrener, A. Bietti, J. Buckman, R. Laroche, J. Bruna. *When Does Return-Conditioned Supervised Learning Work for Offline Reinforcement Learning?* NeurIPS, 2022. (Bando pesimista: fallas de "stitching".)

**Párrafo para el objetivo 5 que las usa:**
> Sobre esta pregunta hay posiciones informadas en desacuerdo: los resultados débiles de dos saltos de [2] y las fallas de "stitching" de la imitación de trayectorias condicionada al retorno (Paster et al. 2022; Brandfonbrener et al. 2022) predicen colapso fuera del soporte de cada demostrador; la generalización composicional documentada en transformers de ajedrez (Mészáros et al. 2025) predice transferencia. La teoría de la mezcla no predice nada aquí porque la señal de entrenamiento es silenciosa, no contradictoria, sobre las posiciones en cuestión: la respuesta es una propiedad del sesgo inductivo del imitador.

### Del dominio (si se confirma cuatro en línea)

- V. Allis. *A Knowledge-Based Approach of Connect-Four*. Tesis de maestría, Vrije Universiteit Amsterdam, 1988. (Resolución del juego.)
- P. Pons. *Connect 4 Game Solver*. http://connect4.gamesolver.org, 2019. (Solver exacto usado.)

### Para las líneas que la sección "Fundamentos" nombra sin citar

- Aprendizaje por imitación y sus límites: S. Ross, D. Bagnell. *Efficient Reductions for Imitation Learning*. AISTATS, 2010; S. Ross, G. Gordon, D. Bagnell. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning* (DAgger). AISTATS, 2011.
- Ensambles y sabiduría de las masas: L. Breiman. *Bagging Predictors*. Machine Learning, 1996; L. S. Marcolino, A. X. Jiang, M. Tambe. *Multi-agent Team Formation: Diversity Beats Strength?* IJCAI, 2013 (es la referencia que [1] usa para "la diversidad vence a la fuerza").
- Robustez al ruido de etiquetas (la discusión sobre filtrar ruido en entrenamiento): D. Rolnick, A. Veit, S. Belongie, N. Shavit. *Deep Learning is Robust to Massive Label Noise*. arXiv:1705.10694, 2017.
- Representación interna del tablero en modelos que solo ven jugadas (sostiene la decisión 6): A. Karvonen. *Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models*. arXiv:2403.15498, 2024; S. Toshniwal et al. *Chess as a Testbed for Language Model State Tracking*. AAAI, 2022. (Ambas citadas por [1].)

### Secundarias (solo si se discute por qué no se intenta reparar relaciones simétricas)

- L. Berglund et al. *The Reversal Curse*. arXiv:2309.12288, 2023.
- Z. Allen-Zhu, Y. Li. *Physics of Language Models: Part 3.2, Knowledge Manipulation*. arXiv:2309.14402, 2023.
- K. Krestnikov. *Truth as a Compression Artifact in Language Model Training*. arXiv:2603.11749, 2026 (verificado el ID; es el trabajo empírico más cercano sobre errores coherentes vs. aleatorios en dominio sintético).
</AI-CONTENT-NOT-CURATED>