## Title

"Properties of transcendence in generative models trained by imitation: a controlled study in a synthetic sequential decision-making domain with exact verification."

## Motivation and objectives

The recent work (2024) by Zhang et al. \[1\] shows a counterintuitive behavior: a model trained on chess games by players with rating \<= 1000[^1] plays at \~1500[^2].

The work calls this phenomenon *"transcendence"*.

In a second publication \[2\], Abreu et al. analyze *transcendence* in a synthetic knowledge-graph domain.

Our objective is to shed light on aspects of the phenomenon not covered by the literature. In particular, regarding:

- Quantifying how the correlation of the experts' errors affects the phenomenon.  
- Testing the impact of composition among experts with disjoint skills (\[2\] obtains weak results in this regard, and the neighboring literature predicts opposite outcomes: collapse outside the support of each demonstrator \[5, 6\] or compositional transfer \[4\]).  
- Measuring the difference in the magnitude of *transcendence* between positions seen or not seen during training.[^3]  
- Differentiating ourselves from \[2\] (which also analyzes properties of transcendence in synthetic domains) through a "sequential-state domain" (in which one decision affects future decisions, as in the chess of \[1\]). This is in contrast to a "static domain" such as the synthetic knowledge graph used in \[2\].

Our domain will be:

- A synthetic domain that we can control (like that of \[2\]).  
- A perfect-information game (an analysis more faithful to \[1\], where the original idea of the concept of *transcendence* is presented).  
- But unlike \[1\], we propose choosing a solved game so that we can have an exact verifier.[^4]

## Foundations and state of knowledge on the subject

The object of study is generative models[^5] trained with the standard imitation objective: minimizing the cross-entropy with respect to the data that trains them.

Theory tells us that in the limit[^6] they learn the distribution of the data.

As mentioned, \[1\] shows that a model trained to imitate a population of "experts" can perform better than the best individual expert in that population.

Concretely, they train a transformer on chess games by players with rating \<= 1000 and the resulting model can play[^7] at \~1500.

They call this phenomenon *transcendence*, and attribute it to the trained model cancelling out uncorrelated errors among the experts.

Abreu et al. \[2\] (testing on a synthetic knowledge-graph domain) analyze three proposed mechanisms of *transcendence*:[^8]

- Denoising by vote.  
- Selection of the competent source.  
- Composition of disjoint knowledge across sources.

### Adjacent areas of the literature

The phenomenon of transcendence sits at the intersection of several well-known lines of work:

- Imitation learning (behavioral cloning) and its theoretical limits \[9, 10\].  
- Ensemble methods (bagging, majority voting) \[11\].  
- The "wisdom of the crowds" literature \[12\].  
- The discussion about whether language models trained on data with systematic errors or biases can filter out that noise during training or sampling \[13\].  
- Memorization dynamics: it is known that a model trained for a sufficient number of passes over a finite dataset eventually memorizes particularities of the sample (including noise) instead of the underlying distribution \[3\].

## Methodology and work plan

It is proposed to make weekly deliveries with a copy to the advisor (Dante Zanarini) and the co-advisor (Pablo Granitto).

&nbsp;

The advisor will monitor the overall progress of the work and supervise the final writing of the report.

&nbsp;

The co-advisor \-from his expertise in machine learning and particularly in deep learning- will supervise at a conceptual level that the hypotheses make sense and are up to the standard of a thesis, that the proposed experiments are methodologically sound, that their specifications do not omit relevant details, and that the results are presented in a coherent and complete manner.

&nbsp;

The work is fundamentally experimental. Preliminary experiments already show that the proposed direction is promising (with positive results).

### Tentative work program

1. The survey of the transcendence literature (and its surrounding framework) has already been carried out for the submission of this proposal. **1 week**  
2. Work will begin on the first experiment until a satisfactory formulation and implementation is reached. This will involve resolving issues common to all the experiments, such as choosing an exact-verification domain, implementing the synthetic generators, implementing the training and evaluation pipeline, etc. **1 week**  
3. Work will be done on a satisfactory presentation of the results of this first experiment. This will be done before continuing with more experiments: having the end-to-end pipeline for one will help iterate with direction on the others. **1 week**  
4. The remaining experiments will be conceptually defined. **1 week**  
5. Work will be done to have the same end-to-end pipeline for each of them. **1 week**  
6. Sensitivity analysis and ablations on the main results; reproducing the results while varying parameters that we assume should not affect them: model size/architecture, amount/representation of the data. **1 week**  
7. By this point, we will already have the complete presentation of results. What remains is to bring them together coherently and formulate conclusions. **1 week**  
8. Only now, having overcome the riskiest part of the work, will we begin writing the Theoretical Framework. An index of sections and subsections will be drawn up with a brief explanation of each: no more than 5 sentences. **1 week**  
9. We will proceed to the full writing of the Theoretical Framework. Everything will be brought together coherently in the final report. **2 weeks**  
10. Corrections will be iterated on until it is polished for presentation and review. **2 weeks**

## REFERENCES

\[1\] E. Zhang, V. Zhu, N. Saphra, A. Kleiman, B. L. Edelman, M. Tambe, S. M. Kakade, E. Malach. *Transcendence: Generative Models Can Outperform The Experts That Train Them*. NeurIPS, 2024\. arXiv:2406.11741.

&nbsp;

\[2\] N. Abreu, E. Zhang, E. Malach, N. Saphra. *A Taxonomy of Transcendence*. COLM, 2025\. arXiv:2508.17669.

&nbsp;

\[3\] D. Arpit, S. Jastrzębski, N. Ballas, D. Krueger, E. Bengio, M. S. Kanwal, T. Maharaj, A. Fischer, A. Courville, Y. Bengio, S. Lacoste-Julien. *A Closer Look at Memorization in Deep Networks*. ICML, 2017\.

&nbsp;

\[4\] A. Mészáros, P. Reizinger, F. Huszár. *Out-of-distribution Tests Reveal Compositionality in Chess Transformers*. arXiv:2510.20783, 2025\.

&nbsp;

\[5\] K. Paster, S. McIlraith, J. Ba. *You Can't Count on Luck: Why Decision Transformers and RvS Fail in Stochastic Environments*. NeurIPS, 2022\.

&nbsp;

\[6\] D. Brandfonbrener, A. Bietti, J. Buckman, R. Laroche, J. Bruna. *When Does Return-Conditioned Supervised Learning Work for Offline Reinforcement Learning?* NeurIPS, 2022\.

&nbsp;

\[7\] V. Allis. *A Knowledge-Based Approach of Connect-Four*. Master's thesis, Vrije Universiteit Amsterdam, 1988\.

&nbsp;

\[8\] P. Pons. *Connect 4 Game Solver*. [http://connect4.gamesolver.org](http://connect4.gamesolver.org), 2019\.

&nbsp;

\[9\] S. Ross, D. Bagnell. *Efficient Reductions for Imitation Learning*. AISTATS, 2010\.

&nbsp;

\[10\] S. Ross, G. Gordon, D. Bagnell. *A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning*. AISTATS, 2011\.

&nbsp;

\[11\] L. Breiman. *Bagging Predictors*. Machine Learning, 24:123–140, 1996\.

&nbsp;

\[12\] L. S. Marcolino, A. X. Jiang, M. Tambe. *Multi-agent Team Formation: Diversity Beats Strength?* IJCAI, 2013\.

&nbsp;

\[13\] D. Rolnick, A. Veit, S. Belongie, N. Shavit. *Deep Learning is Robust to Massive Label Noise*. arXiv:1705.10694, 2017\.

&nbsp;

\[14\] A. Karvonen. *Emergent World Models and Latent Variable Estimation in Chess-Playing Language Models*. arXiv:2403.15498, 2024\.

&nbsp;

\[15\] S. Toshniwal, S. Wiseman, K. Livescu, K. Gimpel. *Chess as a Testbed for Language Model State Tracking*. AAAI, 2022\.

&nbsp;

\[16\] L. Berglund, M. Tong, M. Kaufmann, M. Balesni, A. C. Stickland, T. Korbak, O. Evans. *The Reversal Curse: LLMs Trained on "A is B" Fail to Learn "B is A"*. arXiv:2309.12288, 2023\.

&nbsp;

\[17\] Z. Allen-Zhu, Y. Li. *Physics of Language Models: Part 3.2, Knowledge Manipulation*. arXiv:2309.14402, 2023\.

&nbsp;

\[18\] K. Krestnikov. *Truth as a Compression Artifact in Language Model Training*. arXiv:2603.11749, 2026\.

&nbsp;

&nbsp;

[^1]: \[1\] uses the lichess Glicko-2 rating (similar to Elo). Since chess is not a solved game, Zhang et al. \[1\] use Stockfish as:

    evaluator (with which it computes the "reward per state")

    opponent (games from which the Glicko-2 rating is estimated)

    &nbsp;

[^2]: The same work reports that the model trained on games by players up to 1500 *does not transcend*. It attributes the difference to that dataset having less diversity of moves. Since this is real-game data, one cannot intervene on the correlation structure of the errors. Instead, it measures diversity as the mean entropy of the move distribution in frequent positions and establishes a correlation: for players with rating 1500 this diversity measure is lower than for those with rating 1000\.

    &nbsp;

[^3]: As we explain in the next section, \[2\] attempts to establish a taxonomy of the causes of transcendence. The experiments that evaluate denoising and selection train with noisy experts but all the evaluation is on cases seen in training. In contrast, the generalization experiments evaluate cases not seen in training but fix the experts' error probability at zero. No comparison is posed that shows how the magnitude of transcendence is split between seen and unseen positions in a context where there is noise, such as a game.

[^4]: While probing the feasibility of this work we based the preliminary experiments on "Connect 4" (four in a row) \[7, 8\]; we mention it here although this need not be the game chosen for the work. Even non-game domains with exact verification (for example, certain small combinatorial problems) could serve the same purpose equally well, and the final choice will depend on a balance between the expressiveness of the domain (allowing the experimental conditions of interest to be built) and implementation practicality.

    &nbsp;

[^5]: In particular we will work with autoregressive models. And more specifically with transformer architectures, like the literature on which we build. Also, as in \[1\], the imitator receives only the sequence of moves, never the board, nor the identity of the expert, nor a reward signal. It must internally build a representation of the state from the sequence \[14, 15\].

    &nbsp;

[^6]: "In the limit" means: if we had infinite training data and a model with infinite capacity to represent any function.

    &nbsp;

[^7]: The expression *"can play"* has been chosen deliberately: in the denoising mechanism, \[1\] proves that transcendence is impossible at temperature 1 and requires low-temperature sampling (argmax). For the selection mechanism, in contrast, \[2\] gives a condition under which transcendence already occurs at temperature 1\.

    &nbsp;

[^8]: The mechanisms as we list them follow the terminology created by the authors in Abreu et al. \[2\].
