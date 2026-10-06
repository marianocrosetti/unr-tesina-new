# Summary of [2]

- Paper: https://arxiv.org/abs/2508.17669
- Experiment code (not linked in the paper; it comes from the authors' GitHub):
    - https://github.com/natalieabreu/transcendence: generation of experts and datasets
    - https://github.com/natalieabreu/kg_multihop: contains training and evaluation
    fork of `bellecarrell/twohop` (Annabelle Carrell, mentioned in the acknowledgements), which in turn builds on the RippleEdits code from Cohen et al. 2023. It seems to include only denoising.

## Main idea

- Continue the work of [1] and study why transcendence happens.
- Idea: the trained model imitates a group.
- Transcendence then occurs when the group outperforms each of its members.
- They propose that this happens through three distinct mechanisms (which they call **modes of transcendence**): 

- A model trained by imitation does not imitate *one* person: it imitates a *group*. The group can outperform each member in three different ways.
- The paper formalizes these three ways as **modes of transcendence** and, for each one, gives (a) a condition on the training data and (b) a synthetic experiment that verifies it:
    - **Skill denoising** (error cancellation): all experts talk about everything, each one makes different mistakes, and the majority vote (low temperature) gets it right. This is [1].
    - **Skill selection** (selection / routing): each expert knows about one region; the key is that **they talk more about the region they know**. The model learns to give the answer of the expert who appears most often in that context. Here the errors of the non-experts may be correlated, so the vote can fail anyway.
    - **Skill generalization** (composition): nobody knows the answer to the question; the model combines knowledge from two different experts in a shared latent space.
- The human analogy they use: voting; routing the question to the cryptographer or to the lawyer; a cryptographer and a lawyer reasoning together about the legality of an algorithmic embargo.
- They note that the combination of many people can also **amplify shared biases** (they cite *stochastic parrots*, Bender et al. 2021). The paper studies the other side: when the diversity of the group beats the individual. The motivating example is a chatbot that talks with equal competence about cryptography, international law and Dostoevsky.
- When each mode applies, according to the introduction: denoising when all experts produce data relevant to the input but with independent errors; selection when the input is familiar to *at least one* expert (and that expert encounters it more often); generalization when the input is unfamiliar to *every* expert but can be understood through generalization.
- The overarching thesis: the model transcends only if the set of experts is sufficiently **heterogeneous**. "Diversity" means different things in each mode: uncorrelated errors, varied expertise, varied phrasings and compositions.
- An additional contribution they claim: the *testbed* of a knowledge graph with simulated experts, as a controlled benchmark for future work.
- Domain difference with [1]: there is no game or sequence of decisions. Each query is an isolated fact (head, relation, tail). The ground truth is known by construction (no need for Stockfish).

## Formalization

- They copy the notation of [1] and extend it. Changes:
    - $\mathcal{X} = \mathcal{T}^n$, $\mathcal{Y} = \mathcal{T}^m$: inputs and outputs are sequences of tokens from a vocabulary $\mathcal{T}$.
    - $k$ experts $f_1, \dots, f_k$, **each with its own input distribution** $p_i$. In [1] there was a single $p$ for all of them; this is precisely the simplification that [1] left as future work and that I noted in my summary of [1].
    - The learner chooses within a **hypothesis class** $\mathcal{H}$, not from all of $\mathcal{F}$. This makes it possible to talk about simplicity bias in generalization.
- $\bar p(x) = \frac{1}{k}\sum_i p_i(x)$: average input distribution. $\operatorname{supp}(\bar p)$ is its support.
- **Mixture of experts**, now weighted by state:
$$\bar f(y \mid x) = \sum_{i=1}^{k} g(i \mid x)\, f_i(y \mid x)$$
where $g(i \mid x)$ is "the conditional probability that $x$ was observed under expert $i$".
- The paper does not write the formula for $g$. With a uniform prior over experts (each one generates the same number of samples, which is what they do) it is Bayes:
$$g(i \mid x) = \frac{p_i(x)}{\sum_j p_j(x)} = \frac{p_i(x)}{k\, \bar p(x)}$$
If all the $p_i$ are equal, $g \equiv 1/k$ and the uniform mixture of [1] is recovered.
- Each expert induces $\mathcal{D}_i(x, y) = p_i(x) f_i(y \mid x)$ and the data come from $\bar{\mathcal{D}} = \frac{1}{k}\sum_i \mathcal{D}_i$. One can verify that $\bar{\mathcal{D}}(x,y) = \bar p(x)\, \bar f(y \mid x)$, i.e.: the data amount to "sample $x \sim \bar p$ and label it with the weighted mixture".
- Reward and average reward: same as [1]. $r_x(f) = \mathbb{E}_{y \sim f(\cdot \mid x)}[r(x, y)]$ and $R_p(f) = \mathbb{E}_{x \sim p}[r_x(f)]$.
- **Learner**:
$$h_{\bar{\mathcal{D}}} = \arg\min_{h \in \mathcal{H}} \mathbb{E}_{x \sim \bar p}\big[ H(\bar f(\cdot \mid x),\, h(\cdot \mid x)) \big]$$
This is equivalent to minimizing cross-entropy over $\bar{\mathcal{D}}$. If $\mathcal{H}$ is unrestricted and there is infinite data, $h_{\bar{\mathcal{D}}} = \bar f$.
- **Definition of transcendence**: the same as in [1], $R_{p_{\text{test}}}(h_{\bar{\mathcal{D}}}) > \max_i R_{p_{\text{test}}}(f_i)$.
- The three modes are defined by which assumptions hold:

| Assumption | Denoising | Selection | Generalization |
|---|---|---|---|
| (1) Single input distribution: $p_i = \bar p$ for all | yes | **no** | no |
| (2) In-domain test distribution: $\operatorname{supp}(p_{\text{test}}) \subseteq \operatorname{supp}(\bar p)$ | yes | yes | **no**: $\operatorname{supp}(p_{\text{test}}) \cap \operatorname{supp}(\bar p) = \emptyset$ |

### Skill denoising (formal)
- Assumptions (1) and (2). This is the setting of [1]: at low temperature the mode of the mixture is returned = majority vote; it works if the errors are uncorrelated. They add no new theory.

### Skill selection (formal)
- Assumption (1) is dropped. The experts are *specialists*: each one has an *expertise* = a subset of inputs on which it answers correctly.
- **Claim**: transcendence occurs when a context $x$ is more likely to be observed under the experts that have higher reward on $x$. Formally, $g(i \mid x)$ **depends on $x$** instead of being constant. "The lawyer comments more on questions of law".
- **Theorem 2.1** (two experts $a$ and $b$). For transcendence to hold, we must have:
$$\mathbb{E}_{x \sim p_{\text{test}}}\Big[ \big(r_x(f_a) - r_x(f_b)\big)\,\big(g(a \mid x) - g(b \mid x)\big) \Big] > 0$$
The excess presence of $a$ on $x$ has to be correlated with the excess reward of $a$ on $x$.
- It is a **necessary** condition, not a sufficient one (that is how they state it: "for transcendence to hold, we must have").
- **The proof** (Appendix A.1) assumes $h_{\bar{\mathcal{D}}} = \bar f$ and evaluates **at temperature 1**. With $g(a|x) + g(b|x) = 1$:
$$R(\bar f) - R(f_a) = \mathbb{E}\big[ g(a|x) r_x(f_a) + (1 - g(a|x)) r_x(f_b) - r_x(f_a) \big] = \mathbb{E}\big[ g(b|x)\,(r_x(f_b) - r_x(f_a)) \big] > 0$$
and symmetrically $\mathbb{E}[g(a|x)(r_x(f_a) - r_x(f_b))] > 0$. Adding both gives the statement.
- My notes on the theorem:
    - The two intermediate inequalities are the exact condition (necessary and sufficient given $h = \bar f$); the theorem adds them into a single, weaker one.
    - It is transcendence **at temperature 1**, which [1] proved impossible with a shared $p$. What makes it possible is that $g$ depends on $x$: **Bayesian weighting** of the experts instead of a uniform vote. This confirms the suspicion I noted in my summary of [1].
    - $g$ is defined by the training $p_i$ but the expectation is under $p_{\text{test}}$. In their experiments $p_{\text{test}}$ = uniform over the true facts.
    - There is no theory of selection at low temperature. In the selection experiments they use greedy decoding (see below), so what they measure combines selection (weighting by $g$) with denoising (arg-max). They do not separate the two.

### Skill generalization (formal)
- Assumption (2) is dropped and its opposite is assumed: $\operatorname{supp}(p_{\text{test}}) \cap \operatorname{supp}(\bar p) = \emptyset$. Nothing from the test set was seen in training.
- How can the model answer correctly if no expert can? If the experts' knowledge is representable in a **shared latent space**, the model can compose knowledge from different experts.
- The concrete task: **two-hop fact completion**. Each expert knows one-hop facts and can answer two-hop questions *within* its own knowledge. The test questions need one hop from one expert and the other from another: nobody has both.
- **Hypothesis**: if the learner is biased toward simple solutions, and composing is simpler than memorizing all the two-hop inputs, the model generalizes by composing reusable one-hop components. They formalize this in Appendix A.2 (see its own section below).
- Note: formally, $\max_i R_{p_{\text{test}}}(f_i)$ is trivial here because no expert is defined on the test set. The real bar they compare against is two statistical "shortcut" baselines (see experiments), not the experts.

![Illustration of the expert distributions in the graph. Blue/orange: facts that each expert knows correctly; the rest they get wrong. Opacity is the probability of generating a sample from that edge. In generalization the probability of an incorrect fact is set to 0.](../referencias/mi-review-de-literatura/img/abreu2025/fig1_expert_distributions.png)

- From Figure 1: in generalization the **experts have no errors**. They say so in the caption, not in the text. This is important: the third mode is studied without noise.

## Experiments: details, results and conclusions

### Construction of the knowledge graph (base dataset)

- Ground-truth graph $G = (V, E)$. Nodes = entities, edges = facts (head, relation, tail).
- **Structure** taken from the WIKIDATA-based graph of Cohen et al. 2023 (the *ripple effects* paper on knowledge editing).
- **Entities renamed with fictional names** generated by GPT-4o-mini, to guarantee that the pretrained model never saw those facts. Procedure (Appendix B.1):
    - Fictional country names are requested as a seed and randomly assigned to the countries of the original graph.
    - The graph is traversed in a BFS-like fashion. For each node, GPT-4o-mini is asked for a fictional name using its already-renamed neighbors as context, plus a random starting letter for diversity.
- Size: **~25,000 entities, 39 relation types, 54,500 edges**.
- Each entity has a **semantic type** (country, person, occupation, ...).
- **Incorrect belief = corrupted edge**: a true fact is taken and either the head *or* the tail is replaced by a different entity **of the same type** (so that it remains syntactically plausible). Note: if the head is replaced, the true "(head, relation)" prefix disappears from that expert's data; the paper does not distinguish between the two cases.
- Each expert $i$ has a **personal knowledge graph** $G_i$: a predefined amount of correct knowledge plus incorrect beliefs. How it is built depends on the mode (below).
- For selection and generalization: **spectral clustering over the edges**, **5,000 clusters** = potential areas of expertise. That is ~11 edges per cluster on average. Each expert is assigned knowledge from one or more clusters.

![Example of the graph with fictional entities and two experts. One-hop facts; two-hop facts *within expertise* (known by some expert) and *across expertise* (known by no expert).](../referencias/mi-review-de-literatura/img/abreu2025/fig2_knowledge_graph_example.png)

### How the training data are generated

- Each sample is a **paragraph about an entity**, emulating an expert writing about a topic.
- For $N$ samples with $n_e$ experts, each expert generates $N / n_e$ (unless stated otherwise).
- To generate a sample: a node is sampled **uniformly at random** from the expert's personal knowledge graph, and one templated sentence is written for each edge connected to that node: "The {relation} of {head} is {tail}.". The sentences are written in random order.
- A paragraph includes *all* the edges of the node, correct and corrupted. This is how errors enter the data.
- In terms of the formalization: $p_i$ = distribution induced by "uniform node in $G_i$ + its edges". In denoising all the $G_i$ cover the whole graph, so $p_i \approx \bar p$. In selection the $\alpha$ knob (below) makes $p_i$ concentrate on the expertise.

### Definition of the evaluation method

- Metric: **query completion accuracy**. For each fact in the ground-truth graph, the prompt "The {relation} of {head} is" is built and the output is compared with the tail by **exact match**. If there are several correct tails, any of them counts.
- It is the percentage of true facts that the model **memorized**. The paper says so in those words.
- $p_{\text{test}}$ = uniform over the 54,500 true facts. In denoising and selection it is in-domain by construction: each expert has (correctly or incorrectly) a version of each fact.
- "Expert accuracy" = its coverage $c$: the fraction of true facts it knows. That is the bar for transcendence.
- Decoding: **greedy** (temperature 0) unless the figure shows temperature. Only Figure 3 sweeps temperature.
- They report no seeds, variance or error bars in any figure.

### Training regime

- **Model (denoising and selection)**: *finetuning* of a **pretrained GPT-2**. They do not say which size. **In the code** (`kg_multihop/train/train_2.py`) it is `"gpt2"`, i.e. the small **124M** one. Since the entities are fictional, pretraining contributes no facts from the graph, only language.
- **Model (generalization)**: **LLaMA 3.2 1B** because the task is harder. Preliminary experiments: increasing model size improves two-hop performance only a little (consistent with Yang et al. 2024 and Allen-Zhu & Li 2024b).
- **Objective**: next-token prediction on the paragraphs.
- **Optimization**: AdamW, learning rate $10^{-3}$, weight decay 0.1, 1000 warmup steps, cosine decay, batch size 24. Note: a learning rate of $10^{-3}$ is high for finetuning; they do not justify it.
- **Amount of data per mode**:
    - Denoising: 10M samples per configuration. That is ~400 paragraphs per entity, so each fact receives hundreds of "votes" in the dataset (from the head and from the tail).
    - Selection: 1M paragraphs, 10 epochs.
    - Generalization: 6M one-hop paragraphs + 80,000 two-hop facts repeated 20 times per epoch, 10 epochs.
- **Compute** (Appendix B.2): 1 to 4 H100s for 1 to 8 hours per run.

### Experiment 1: skill denoising

- **Hypothesis**: if each source makes mistakes on different facts, the collective vote is right.
- **Construction of the experts**: all share a **coverage level** $c \in [0, 1]$ = the fraction of the graph that each expert knows correctly. To build $G_i$, each edge of the ground-truth graph is traversed: with probability $c$ the correct edge is included, with $1 - c$ a corrupted version is included.
- **Manipulated variable**: the number of experts $n_e$, **as a proxy for uncorrelated errors**. Since errors are sampled uniformly and independently per expert, more experts → the distribution of errors in the dataset is more uniform (the wrong votes are spread across many different tails, while the correct one concentrates $c$ of the votes).
- With $n_e = 1$ there is nothing to cancel: the single expert's incorrect belief about an edge is deterministic, the model memorizes it, and the accuracy is $c$ at any temperature.
- Note: each individual expert is *not* a "noisy expert" in the sense of Prop. 3 of [1] (uniform noise per state). It is deterministic. The uniform noise emerges at the **population** level. The mechanism is that of Prop. 4 of [1] (complementary experts) with randomly chosen regions.
- **Results**:
    - With enough experts, the individual coverage is far exceeded. With $c = 0.2$ and 100 experts: **over 80 % accuracy**.
    - Figure 4 (coverage vs accuracy, greedy): with 1 expert the curve is the diagonal (accuracy = $c$). With 10 it lies above the diagonal (read off the plot: $c = 0.4 \to$ ~0.58, $c = 0.8 \to$ ~0.93). With 100 and 1000 it saturates at ~1 from $c \approx 0.4$.
    - Figure 3 (temperature vs accuracy, for 1, 10, 100 experts and coverages from ~0.05 to 1; temperatures 0, 1 and 1.5): at low temperature the accuracy goes up; **at temperature 1 it stays close to the coverage level** (the mixture performs like the average expert, as predicted by Prop. 1 of [1]); at 1.5 it drops further. With 1 expert the curves are flat.
- **Paper's conclusion**: diversity in the form of **uncorrelated errors** allows transcending through the "wisdom of the crowd" with low-temperature sampling.

![Denoising: accuracy vs temperature for 1, 10 and 100 experts. Color = coverage.](../referencias/mi-review-de-literatura/img/abreu2025/fig3_denoising_temperature.png)

![Denoising: expert coverage vs accuracy (greedy). Color = number of experts (1 to 1000, log scale).](../referencias/mi-review-de-literatura/img/abreu2025/fig4_denoising_coverage_vs_acc.png)

### Experiment 2: skill selection

- **Motivation**: in reality non-experts share *misconceptions*, their errors are correlated, and the vote guarantees nothing. But the model can still outperform everyone if it gives the answer of the source with the relevant expertise. For that, the data must have each expert **talking more about what they know than about what they do not know**.
- **Construction of the experts**:
    - Shared coverage $c$.
    - Each expert $i$ has a **coverage vector** $s_i = (s_i^{(1)}, \dots, s_i^{(5000)})$ with $s_i^{(j)} \in [0, 1]$ = the expert's accuracy on the edges of cluster $j$, subject to
$$\sum_{j=1}^{5000} s_i^{(j)}\, |C_j| = c \cdot |E|$$
    - For each edge $e \in C_j$: with probability $s_i^{(j)}$ it is included correctly, with $1 - s_i^{(j)}$ it is included corrupted.
    - The paper **does not specify** how the $s_i^{(j)}$ are chosen. **In the code** (`transcendence/src/dataset_generator.py`, `skill_selection`, `select_clusters` and `get_confidence_scores_lp`):
        - Each expert picks clusters **at random** (shuffle) until it gathers `edges_per_expert` edges.
        - The $s_i^{(j)}$ of those clusters come from a **linear program**: maximize $\sum_j s_i^{(j)}$ subject to $\sum_j |C_j|\, s_i^{(j)} = c\,|E|$ and $0 \le s \le 1$. The solution of such an LP falls on a vertex: almost all the $s$ end up at **0 or 1** and at most one is fractional. That is, in practice the expertise is binary per cluster.
        - The clusters not chosen are left with $s = 0$: the expert **always** gets them wrong.
    - Corruption (`get_modified_graph_over_edges`): with probability $1 - s$, either the tail or the head (50/50) is replaced by an entity drawn **uniformly** from those that appear as tail (or head) of that same relation. This is what the paper calls "entity of the same type". The draw is **independent per expert**.
    - Conclusion: the suspicion was correct. The motivation talks about **shared** misconceptions, but what is implemented is "the majority is wrong, each in their own way". What makes the vote fail is not that they agree on the error but that many more of them are wrong.
- **Generation with the $\alpha$ knob**: a node is sampled uniformly from the personal knowledge graph as before, but now each connected fact is written with probability
$$p = \alpha\, s_i^{(j)} + (1 - \alpha), \qquad \alpha \in [0, 1]$$
where $j$ is the cluster of the edge.
    - $\alpha = 1$: writes each fact with probability equal to its expertise on that cluster. If $s \in \{0, 1\}$, the expert **writes only what it knows** and the dataset has no noise.
    - $\alpha = 0$: writes everything equally, what it knows and what it does not.
    - $\alpha$ is the knob for **how much each expert talks about what it does not know**. It controls how concentrated $p_i$ is on the expertise, i.e. how much $g(i \mid x)$ depends on $x$.
- **Results** (1M paragraphs, 10 epochs; coverages $c \in \{0.01, 0.1\}$; $\alpha \in [0.8, 1]$; 1 to 1000 experts; Figure 5):
    - For both coverages, with enough experts the accuracy reaches nearly 1.
    - Accuracy improves consistently with $\alpha$.
    - With $c = 0.01$ the transition is **abrupt**: accuracy is ~0.1 for $\alpha \le 0.95$ and only at $\alpha = 1$ does it rise (1000 experts: ~1.0; 100 experts: ~0.65).
    - With $c = 0.1$ it is gradual: 100 experts go from ~0.7 ($\alpha = 0.8$) to ~1.0 ($\alpha = 1$); 10 experts from ~0.1 to ~0.5; 1 expert stays flat at ~0.05.
    - The paper interprets "more experts = more diversity of expertises".
- **Paper's conclusion**: with biased errors, transcendence is enabled by diversity of **expertises**. To guarantee it, experts must write more about their own domain than outside it.

![Selection: $\alpha$ vs accuracy for coverages 0.01 and 0.1. Color = number of experts.](../referencias/mi-review-de-literatura/img/abreu2025/fig5_selection_alpha_vs_acc.png)

- My notes and calculations on this experiment:
    - **Ceiling without generalization**: accuracy cannot exceed the fraction of the graph that *some* expert knows. If clusters are assigned randomly and independently, that is $\approx 1 - (1 - c)^{n_e}$. It gives 0.63 for $(c, n_e) = (0.01, 100)$ and 0.65 for $(0.1, 10)$; in Figure 5 those cases reach ~0.65 and ~0.5 at $\alpha = 1$. This is consistent with the model memorizing, at $\alpha = 1$, the union of what everyone knows. To cover the graph you need $n_e \cdot c \gtrsim 1$, and that explains which curves take off.
    - **Why the transition is abrupt with $c = 0.01$**: for a given fact, ~$n_e c$ experts know it and always write it ($p = 1$); the other ~$n_e(1 - c)$ know it wrong and write it with probability $1 - \alpha$. With $(c, n_e) = (0.01, 100)$ there is 1 correct vote against $99(1 - \alpha)$ wrong votes: 5 at $\alpha = 0.95$, 10 at $\alpha = 0.9$. Even if the wrong ones are spread across different tails, 1 correct vote is rarely the plurality. With $c = 0.1$ it is 10 correct votes against $90(1 - \alpha)$ and the transition is gradual. This is a threshold argument on the **proportion of votes**, analogous to the $\alpha^*$ of my experiment 2.
    - With $\alpha = 1$ and $s \in \{0, 1\}$ there is **no noise in the dataset**, so the "transcendence" is that the model memorizes the union of knowledge. It is the extreme case of Prop. 4 of [1] but without the need for low temperature: the non-experts stay silent, and $g(i \mid x)$ concentrates on the expert. The interesting part is $\alpha < 1$, and there what resolves it is the arg-max (greedy), i.e. selection **plus** denoising.
    - They only sweep $\alpha \in [0.8, 1]$. Below 0.8 it presumably does not work; they do not show it.

### Experiment 3: skill generalization

- **Idea**: in selection at least one expert knows the answer; here **none** does. The model has to compose knowledge from two experts using shared representations.
- **Construction of the experts**: simplified version of selection. **Each expert knows a single cluster** and **has no errors** (Figure 1). The paper does not say how many experts there are. **In the code** (`per_cluster_strategy`): expert $i$ is exactly cluster $i$, with one-hot expertise and a personal graph made only of the edges of that cluster (there are no corrupted edges). With `num_experts = n`, clusters $0, \dots, n-1$ are used; there is no way to know which $n$ they used in the paper. There is a special single-expert case that uses cluster 4999, commented as "baseline with the largest cluster". Each expert generates samples **in proportion to the size of its cluster** (here it does depart from the uniform $N / n_e$).
- **Evaluation framework**: that of Yang et al. 2024 (*Do LLMs latently perform multi-hop reasoning?*). **Latent** compositional ability = answering the two-hop fact **without generating the intermediate entity**, given that the one-hop facts are known.
- **Two types of two-hop facts**:
    - **Within-expertise**: both edges are in the same cluster. Some expert knows both hops.
    - **Across-expertise**: the two edges are in different clusters. Nobody knows both.
- **Data**: 6M one-hop paragraphs (as before) + a set of **within-expertise two-hop** facts written as sentences, to **teach the two-hop format**. Its size is swept: 20,000, 40,000, 60,000, **80,000** (all of them). They are repeated 20 times per epoch to saturate training accuracy. 10 epochs.
- **Evaluation sets**:
    - One-hop: all the facts.
    - **Within-expertise validation**: ~6,000 held-out within-expertise two-hop facts (6,133 according to B.3.1). Measures composition *without crossing experts*.
    - **Across-expertise test**: **64,811** facts. Never seen as two-hop, and they also require crossing experts. This is the generalization test.
- **"Shortcut" baselines** (from Yang et al. 2024), because the "best expert" bar is trivially 0 here:
    - *Direct connection*: is there a direct head–tail edge in the one-hop facts? It counts head–tail pairs that co-occur: 528/6,133 = **0.086** in validation, 5,666/64,811 = **0.087** in across. They also checked head–tail co-occurrence in the two-hop training set: <5 %, which they omit.
    - *Majority relation* (called "Relation Majority" in the figures): answer with the most frequent entity of the correct type for the second relation: **0.20** across, **0.15** within.
- **Results** (Figure 6 across; Figure 7 within, in the appendix):
    - One-hop: near-perfect in all models.
    - Across-expertise grows **roughly linearly** with the number of two-hop examples in training: ~0.25 (20,000) → **0.34** (80,000). Versus 0.20 for majority relation.
    - Within-expertise (validation): 0.36 → **0.70** over the same range.
    - My reading: composing two facts from the *same* expert is already hard (0.70), and crossing experts costs about as much again (0.34). The difference 0.70 vs 0.34 isolates the cost of crossing experts from the cost of composing.
    - **Central challenge** they state: the number of two-hop facts that an individual expert knows is **finite** (it is bounded by the within-cluster ones). The set cannot keep growing. That is why they try two alternatives.

![Generalization, across-expertise. Left: accuracy vs number of two-hop examples in training. Right: comparison of methods with the full 80,000.](../referencias/mi-review-de-literatura/img/abreu2025/fig6_generalization_across_expertise.png)

![Generalization, within-expertise (held-out validation). Same panels as the previous figure.](../referencias/mi-review-de-literatura/img/abreu2025/fig7_generalization_within_expertise.png)

#### Alternative A: phrasing diversity
- Inspired by Allen-Zhu & Li 2024a (*Physics of LMs 3.1*): data augmentation through rewriting makes the model form better latent representations instead of memorizing context.
- **Four diversity levels** (Table 1 of the paper), one for each one-hop paragraph:
    1. One template per relation (the standard).
    2. Four templates per relation, one is chosen at random for each edge.
    3. GPT-4o-mini rewrites the level 1 paragraph with low creativity. Prompt: "You will be provided with a list of facts about an entity. Your job is to write a 10-50 word encyclopedia entry about the given entity. You should not make up additional information, just rewrite the facts."
    4. GPT-4o-mini rewrites the level 2 paragraph with high creativity. Same prompt plus "Use creative word choices and phrasing."
- At levels 1 and 2 the two-hop facts are written in a single template. To diversify them, GPT-4o-mini is asked to rephrase each two-hop sentence.
- "Data diversity" models: **1.5M distinct paragraphs × 4 levels = 6M samples**. Same total as the standard (6M), so same compute but 4 times fewer sampled nodes. Plus the rephrased two-hop facts repeated 20×/epoch along with the templated ones.
- **Result**: diversity in the **one-hop** paragraphs: across 0.34 → **0.37** (within 0.70 → 0.79). Diversity in the **two-hop** facts: **no effect**. They leave more principled augmentations for future work.

#### Alternative B: Chain-of-Thought
- Previous works (Wei et al. 2023; Allen-Zhu & Li 2024b; Prystawski et al. 2023) find CoT essential for knowledge manipulation and multi-hop.
- **Format** (B.3.4): QA with the intermediate entity before the final answer, separated by a semicolon. Example: "What is the award received by the screenwriter of Glyndor Aetheralis? Ithryndor Glaciaris; Xyphorian Starblossom." At evaluation time the model is allowed to generate the intermediate step and **only the final answer** is judged.
- **Result**: across **0.62**, within 0.92.
- **Conceptual observation of the paper**: when the model explicitly names the intermediate node, it **reduces the generalization problem to a selection one**: each hop separately is known by some expert. That is why CoT helps so much. And that is why 0.62 is not evidence of latent composition.
- **Paper's conclusion on generalization**: it is the hardest mode but LMs do achieve it (partially). It is promoted by diversity of surface forms and, more noticeably, by **diversity of compositions** in the training data. They themselves call it a "nontrivial improvement over the 20% baseline".

### Formal analysis of generalization (Appendix A.2)

- Case study to give intuition for why a learner with a simplicity bias prefers to compose. Based on the graph setting.
- $G = (V, E)$, $R$ relation types, edge $e = (a, r, b)$. $F^{(1)} = E$ = one-hop facts. **Assumption**: deterministic mapping, for each prefix $(a, r)$ there is at most one $b$. They call $(a, r)$ a "one-hop input".
- Two-hop fact $(a, r_1, r_2, c)$ with bridge entity $b$: $(a, r_1, b), (b, r_2, c) \in F^{(1)}$. Set $F^{(2)}$. Function $f^*: V \times R \times R \to V$ defined only where a bridge exists. $(a, r_1, r_2)$ is a "two-hop input".
- $f^*$ is **compositional**: $f^*(a, r_1, r_2) = g^*(g^*(a, r_1), r_2)$ with $g^*(a, r) = b$.
- $\mathcal{X}$ = valid two-hop inputs. $\mathcal{Y} = V \cup \{\epsilon\}$, with $\epsilon$ a null label.
- Partition of the one-hop facts into $k$ experts $F_i^{(1)}$. Input space of expert $i$:
$$\mathcal{X}_i = \{ (a, r_1, r_2) \mid \exists\, b, c : (a, r_1, b), (b, r_2, c) \in F_i^{(1)} \}$$
(both edges in its partition). $p_i$ with full support on $\mathcal{X}_i$. The expert always labels correctly. Dataset $D$ of $N$ unique samples.
- Hypothesis class $\mathcal{H} = \mathcal{H}_{\text{mem}} \cup \mathcal{H}_{\text{comp}}$:
    - Memorizers: a table $T^{(2)}$ of size $V \times R \times R$, $h(a, r_1, r_2) = T^{(2)}[(a, r_1, r_2)]$.
    - Compositional: a table $T^{(1)}$ of size $V \times R$, $h(a, r_1, r_2) = g(g(a, r_1), r_2)$ with $g(a, r) = T^{(1)}[(a, r)]$.
- **Complexity** $\kappa(T)$ = number of non-null entries of the table. Composing has a fixed overhead: $\kappa(f(f(\cdot), \cdot)) = \kappa(f) + \kappa_{\text{comp}}$.
- ERM: $h_D \in \arg\min_{h \in \mathcal{H}} \mathbb{E}_{(x, y) \sim D}[H(y, h(x))]$. It is realizable, so there is a set $\mathcal{H}^*_D$ of zero-loss hypotheses. Any memorizer of $D$ is in it, but this says nothing about two-hop facts across partitions.
- **Simplicity bias**: $h_D \in \arg\min_{h \in \mathcal{H}^*_D} \kappa(h)$.
- Memorizer: $\kappa(h) \geq |D|$. Compositional: $\kappa(h) \leq |F^{(1)}| + \kappa_{\text{comp}}$.
- **Sufficient condition** for the learner to prefer composing: $|D| \geq |F^{(1)}| + \kappa_{\text{comp}}$. (Strictly it should be $>$ for the preference to be strict.)
- **Bound on $|D|$**: in training there are only within-partition two-hop facts. With $d_{\text{in}}(v)$ and $d_{\text{out}}(v)$ the degrees of $v$: $|F^{(1)}| = \sum_v d_{\text{in}}(v) = \sum_v d_{\text{out}}(v)$. Each node induces $d_{\text{in}}(v) \cdot d_{\text{out}}(v)$ two-hop facts. Then
$$|D| \leq \sum_{i=1}^{k} |\mathcal{X}_i| = \sum_{i=1}^{k} \sum_{v \in V} d^{(i)}_{\text{in}}(v)\, d^{(i)}_{\text{out}}(v)$$
with degrees restricted to the edges of partition $i$.
- **Final condition**:
$$\sum_{v \in V} d_{\text{in}}(v) + \kappa_{\text{comp}} < \sum_{i=1}^{k} \sum_{v \in V} d^{(i)}_{\text{in}}(v)\, d^{(i)}_{\text{out}}(v)$$
Intuition: there must exist enough valid two-hop facts **within the domain of a single expert**. Since the knowledge lives in a shared latent space (reusable one-hop representations), composing is cheap and the learner prefers to generalize.
- My notes:
    - The condition depends on the **granularity of the partition**: finer partitions (more clusters, fewer edges per cluster) shrink the right-hand side. With 5,000 clusters for 54,500 edges, the within-cluster two-hop facts are ~86,000 (80,000 + 6,133) versus 64,811 across. Spectral clustering groups densely connected edges, which is why there are so many within.
    - The experiment of Figure 6 (growing the two-hop set) **manipulates the $|D|$ side** of the inequality. This is what they call "motivated by our analysis in Appendix A.2". They verify neither the simplicity bias itself nor $\kappa_{\text{comp}}$.
    - In the formal model there are no one-hop paragraphs in the training set (only two-hop inputs); in the experiment there are, and the model knows all the one-hop facts (accuracy ~1). So the experiment is easier than the formal model in that respect.

## Verification against the code

I reviewed both repos (2026-10-05). What it confirms, contradicts or adds with respect to the paper:

- **Batch size 24** = `per_device_train_batch_size: 8` × `gradient_accumulation_steps: 3` (`kg_multihop/train/train_2_config.yaml`), on 1 GPU. With more GPUs it would be larger; the paper does not clarify. Learning rate 0.001, weight decay 0.1 and warmup 1000 match.
- **Sequences**: padding to `max_length=512` and truncation. Each paragraph is an independent example (no packing).
- **Evaluation** (`eval/cloze_task.py`): greedy with `max_new_tokens=20`. From the generated text, what comes before the first period is taken, the prompt is removed, and it is marked correct if that string is **exactly** in the list of valid answers. This is the paper's exact match.
- **Temperature**: at each evaluation the trainer reports two accuracies, greedy and temperature 1. Figure 3 comes from there plus some runs at 1.5.
- **Denoising**: the configs available (`train/data_files.json`) use `entities_per_expert = 25803` (all the entities) and `confidence` = $c$. So each expert covers the whole graph with probability $c$ of being correct per edge, which is what the paper describes. There are configs with $c \in \{0.6, 0.8, 1.0\}$ and 1, 10 and 1000 experts.
- **Template ablations** not reported in the paper: there are configs with `original_entities` (real Wikidata names instead of fictional ones), `spo_templates` and `all_templates`. I do not know what they yielded.
- **Selection paragraph** (`kg.get_skill_selection_paragraph`): for each edge entering or leaving the node it is written with probability $\alpha s + (1-\alpha)$, as in the paper. It includes edges where the node is the tail, not only the head.
- **Selection experts**: random choice of clusters + linear program (see Experiment 2). Clusters not chosen have $s = 0$.
- **Corruption**: tail or head at 50 %, uniform among entities used with that relation, independent per expert.
- **Generalization**: one expert per cluster, no errors. The two-hop facts are built by joining edges of a cluster with itself (within) or with another (across). The rephrasing of the two-hop facts uses GPT-4o-mini with a short system prompt ("Please rephrase the sentence") and two few-shot examples.
- **Not included**: the script that runs each figure, the exact values of `edges_per_expert` in selection, the $n$ for generalization, the LLaMA 3.2 1B code and the CoT code, and the fictional graph itself.
- **Seeds**: the code accepts a seed for generating data, but the paper does not report multiple runs.

## Related work they cite (useful for my theoretical framework)

- **Transcendence**: [1]; Cunningham 2023 (blog post *An AI which imitates humans can beat humans*) also outlined ways in which an imitator outperforms the human.
- **Data diversity and knowledge acquisition**: Allen-Zhu & Li 2024a (synthetic biographies; augmentation → flexible extraction); Zhu et al. 2025 (diverse formats improve acquisition); Allen-Zhu & Li 2024b (CoT critical for knowledge manipulation); Naik et al. 2024 (diversity of prompting at inference); Chang et al. 2024 (fictional entities to study acquisition over the course of training); compositionality and diversity: Berlot-Attwell et al. 2024, Levy et al. 2023, Oren et al. 2021, Rahimi et al. 2024.
- **Failures of composition in transformers**: Dziri et al. 2023 (*Faith and Fate*); Press et al. 2023 (*compositionality gap*, which does not shrink with scale); Wang et al. 2024 (path finding: they do not learn reachability through transitivity); Yang et al. 2024 (scale helps the first hop, not the second); Saparov et al. 2023.
- **Generalization / implicit regularization**: Goldblum et al. 2024 (bias toward low Kolmogorov complexity); Zadrozny 2000 (MDL: memorizing becomes high-complexity as the corpus grows and composition emerges).
- **Ensembling and model fusion**: the model can be seen as an **implicit ensemble** of the experts that generated its data. Majority voting over outputs (Wang et al. 2023 *self-consistency*; Li et al. 2024 *more agents is all you need*); MoE (Lepikhin 2020 GShard, Fedus 2022 Switch) and ensembles (Liu 2021 DExperts, Li 2022 Branch-Train-Merge, Gururangan 2023 c-BTM) design selection into the **architecture**; here the experts are in the **data** and the architecture is a single network. Fusion (Wan 2024, Mavromatis 2024). Li 2022 and Gururangan 2023 train separate models on clusters of documents and combine them at inference.

## Limitations they state

- The synthetic setup isolates phenomena but is limited; they call for work in more realistic settings.
- The framework does **not capture *skill discovery***: producing something that no expert knows and that cannot be obtained by composing what they know.
- On generalization: the results are modest (34 % vs 20 % baseline) and they acknowledge it.

## Positioning of my work with respect to [2]

(My draft, to be reviewed.)

### What my work takes from [2]

- The **taxonomy** as an organizing framework: my objectives 1, 2 and 5 are the three modes. Objective 3 (temperature) and objective 4 (seen vs unseen) are cross-cutting cuts that [2] does not make.
- The formalization with $p_i$ per expert and $g(i \mid x)$: it is the one that fits my setting, where each expert's policy induces its own distribution of states.
- The $\alpha$ knob of selection is analogous to my routing $\alpha$ of experiment 2. The threshold argument by proportion of votes (my calculation above) is the same as that of my $\alpha^*$.
- The **shortcut baselines** for generalization: in my experiment 4 I need an analogous bar, because "the best expert" is not defined on the test set either.

### Limitations of [2] that my domain covers

- **Static domain**: each query is an isolated fact. There is no sequence of decisions or a state that a move conditions. In Connect 4 the error of a move is paid for later.
- **Test always in-domain, and memorization**: in denoising and selection the metric is literally "percentage of memorized facts". They do not separate seen from unseen states (my objective 4). In generalization the test is 100 % unseen but with **error-free** experts. There is no cell with noise and unseen states at the same time, which is what is natural in a game with imperfect experts.
- **Error correlation not controlled**: in denoising they use $n_e$ as a *proxy* for decorrelation; they never directly set the proportion of shared errors (my objective 1, parameter $P$). In selection the motivation talks about shared misconceptions but the implementation corrupts randomly per expert.
- **Selection and denoising not separated**: the selection theory is at temperature 1, the experiments are greedy. There is no temperature curve for selection. My objective 3 is exactly that.
- **Generalization**: weak results (0.34 vs 0.20), and CoT reduces it to selection. My experiment 4 (families A/B with disjoint support) attacks the same thing in a domain where composing means playing an entire game well.
- **Reproducibility**: the code is not linked and is incomplete (no launch scripts or graph), no seeds reported, no error bars.

### Methodological decisions and checks that [2] suggests to me

- Always report the **expert bar** next to the model's in the same plot (they do it implicitly with the diagonal of Figure 4). In my case: score of the best expert vs score of the model, per configuration.
- Compute the **ceiling without generalization** of each configuration (what fraction of the test set *some* expert knows), as I did above with $1 - (1 - c)^{n_e}$. In selection it separates "memorized the union" from "truly transcended".
- For experiment 4, define explicit **shortcut baselines** (play randomly among legal moves, repeat the most frequent move per phase, etc.), not just "best expert".
- Report the number of **votes per state** in the dataset (they have ~400 paragraphs per entity in denoising). In Connect 4 that drops with depth and is part of what objective 4 will measure.
- Run **several seeds**. They do not, and it is the easiest criticism to avoid.

### DOUBTS

- In selection with $\alpha < 1$ and greedy decoding, how much of what they measure is $g(i \mid x)$ and how much is arg-max? If they repeated Figure 5 at temperature 1 it would show. Is it worth my running that cell (selection at $\tau = 1$) as an explicit control for Theorem 2.1?
- Theorem 2.1 is only for two experts. Is there a version for $k$ experts? For my experiment 2 with $K = 4$ I would need to generalize it (the exact condition is $R(\bar f) > R(f_i)$ for each $i$, with $\bar f$ the mixture weighted by $g$).
- How does "talking more about what one knows" translate to a game? In Connect 4 an expert does not choose which states to play on: the states come to it. My routing $\alpha$ (which expert plays in which region) is the translation, but it is worth making explicit that the knob is in the **data generator**, not in the expert.
- In generalization each expert is a cluster (confirmed in the code), i.e. ~11 edges on average. I do not know how many they used. If it was all 5,000, the "expertise" of each one is tiny. It affects how to compare with my families A/B, which are two large subpopulations.
